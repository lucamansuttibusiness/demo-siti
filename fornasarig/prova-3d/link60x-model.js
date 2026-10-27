// Link 60X: ricostruzione parametrica indicativa (metri), fatta a occhio dalle foto prodotto.
import * as THREE from 'three';

const ROD_R = 0.0055;              // tondino pieno Ø 11 mm (dato ufficiale)
const HALF_W = 0.222;
export const STACK_STEP = 0.0192;  // 60 sedie in meno di 2 m (dato ufficiale) → passo ≈ 19 mm
export const STACK_DZ = 0.0015;

function roundedPath(pts, r) {
  const path = new THREE.CurvePath();
  let last = pts[0].clone();
  for (let i = 1; i < pts.length - 1; i++) {
    const p = pts[i], a = pts[i - 1], b = pts[i + 1];
    const din = p.clone().sub(a), dout = b.clone().sub(p);
    const rr = Math.min(r, din.length() / 2, dout.length() / 2);
    const s = p.clone().sub(din.normalize().multiplyScalar(rr));
    const e = p.clone().add(dout.normalize().multiplyScalar(rr));
    if (last.distanceTo(s) > 1e-5) path.add(new THREE.LineCurve3(last, s));
    path.add(new THREE.QuadraticBezierCurve3(s, p.clone(), e));
    last = e;
  }
  path.add(new THREE.LineCurve3(last, pts[pts.length - 1].clone()));
  return path;
}

function shell(fn, nu, nv, offset) {
  const pos = [], idx = [];
  const grid = (off) => {
    const base = pos.length / 3;
    for (let j = 0; j <= nv; j++) for (let i = 0; i <= nu; i++) {
      const [x, y, z] = fn(i / nu, j / nv);
      pos.push(x + off[0], y + off[1], z + off[2]);
    }
    return base;
  };
  const top = grid([0, 0, 0]), bot = grid(offset);
  const id = (b, i, j) => b + j * (nu + 1) + i;
  for (let j = 0; j < nv; j++) for (let i = 0; i < nu; i++) {
    idx.push(id(top, i, j), id(top, i + 1, j), id(top, i, j + 1), id(top, i + 1, j), id(top, i + 1, j + 1), id(top, i, j + 1));
    idx.push(id(bot, i, j), id(bot, i, j + 1), id(bot, i + 1, j), id(bot, i + 1, j), id(bot, i, j + 1), id(bot, i + 1, j + 1));
  }
  const ring = [];
  for (let i = 0; i <= nu; i++) ring.push([i, 0]);
  for (let j = 1; j <= nv; j++) ring.push([nu, j]);
  for (let i = nu - 1; i >= 0; i--) ring.push([i, nv]);
  for (let j = nv - 1; j >= 1; j--) ring.push([0, j]);
  for (let k = 0; k < ring.length; k++) {
    const [i0, j0] = ring[k], [i1, j1] = ring[(k + 1) % ring.length];
    const a = id(top, i0, j0), b = id(top, i1, j1), c = id(bot, i0, j0), d = id(bot, i1, j1);
    idx.push(a, c, b, b, c, d);
  }
  const g = new THREE.BufferGeometry();
  g.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3));
  g.setIndex(idx);
  g.computeVertexNormals();
  return g;
}

const corner = (v, r) => {
  const t = Math.max(0, Math.abs(2 * v - 1) - (1 - r)) / r;
  return Math.sqrt(Math.max(0, 1 - t * t * 0.55));
};

export function buildGeometries() {
  const seat = shell((u, v) => {
    const w = 0.432 * corner(v, 0.22), s = 2 * u - 1;
    let y = 0.462 - 0.013 * (1 - s * s) * Math.sin(Math.PI * Math.min(v, 0.85) / 0.85) + 0.006 * s * s;
    if (v > 0.84) y -= 0.034 * Math.pow((v - 0.84) / 0.16, 2);   // bordo a cascata
    if (v < 0.08) y += 0.01 * Math.pow((0.08 - v) / 0.08, 2);
    return [s * w / 2, y, -0.165 + v * 0.395];
  }, 22, 24, [0, -0.006, 0]);

  const back = shell((u, v) => {
    const y = 0.505 + v * 0.335;
    let w = 0.392 + 0.07 * Math.pow(v, 0.8);
    if (v > 0.82) w *= Math.sqrt(1 - Math.pow((v - 0.82) / 0.18, 2) * 0.32);
    if (v < 0.06) w *= 0.97;
    const s = 2 * u - 1;
    return [s * w / 2, y, -0.17 - (y - 0.5) * 0.19 + 0.036 * s * s + 0.012 * Math.sin(Math.PI * v)];
  }, 22, 24, [0, 0, -0.0042]);

  const side = (x) => roundedPath([
    new THREE.Vector3(x, 0.836, -0.208),
    new THREE.Vector3(x, 0.47, -0.150),
    new THREE.Vector3(x, 0.012, -0.222),
    new THREE.Vector3(x, 0.012, 0.212),
    new THREE.Vector3(x, 0.446, 0.200),
    new THREE.Vector3(x, 0.446, -0.142)
  ], 0.038);
  const bar = (a, b) => new THREE.TubeGeometry(new THREE.LineCurve3(a, b), 2, ROD_R, 8, false);
  const rods = [
    new THREE.TubeGeometry(side(-HALF_W), 140, ROD_R, 8, false),
    new THREE.TubeGeometry(side(HALF_W), 140, ROD_R, 8, false),
    bar(new THREE.Vector3(-HALF_W, 0.165, 0.208), new THREE.Vector3(HALF_W, 0.165, 0.208)),
    bar(new THREE.Vector3(-HALF_W, 0.446, 0.02), new THREE.Vector3(HALF_W, 0.446, 0.02))
  ];
  const glide = new THREE.CylinderGeometry(0.009, 0.009, 0.012, 16);
  const glidePos = [[-HALF_W, 0.006, 0.175], [HALF_W, 0.006, 0.175], [-HALF_W, 0.006, -0.185], [HALF_W, 0.006, -0.185]];
  return { seat, back, rods, glide, glidePos };
}

export function buildChair(geo, mats) {
  const g = new THREE.Group();
  const add = (geom, mat) => { const m = new THREE.Mesh(geom, mat); m.castShadow = true; m.receiveShadow = true; g.add(m); return m; };
  add(geo.seat, mats.shell); add(geo.back, mats.shell);
  geo.rods.forEach(r => add(r, mats.frame));
  geo.glidePos.forEach(p => add(geo.glide, mats.glide).position.set(p[0], p[1], p[2]));
  return g;
}
