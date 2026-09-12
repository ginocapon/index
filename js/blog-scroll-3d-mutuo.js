/**
 * Mutuo under 36 — showcase 3D (rebuild)
 * Paesaggio 3D · casa centrale · rotazione 1:1 con scroll
 */
(function () {
  'use strict';

  var CFG = { turns: 3.5 };

  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var mobile = window.matchMedia('(max-width:768px)').matches;

  var wrap = document.getElementById('mutuo-canvas-wrap');
  var layer = document.querySelector('.b3d-scroll-layer');
  var loading = document.querySelector('.b3d-loading');
  var hint = document.querySelector('.b3d-scroll-hint');
  var bar = document.querySelector('.b3d-progress');

  if (!wrap || typeof THREE === 'undefined') {
    if (loading) loading.textContent = 'Scena 3D non disponibile';
    return;
  }

  var scene = new THREE.Scene();
  scene.background = new THREE.Color(0x0d1117);
  scene.fog = new THREE.Fog(0x0d1117, 18, 48);

  var camera = new THREE.PerspectiveCamera(38, innerWidth / innerHeight, 0.1, 80);
  var camDist = mobile ? 11.5 : 9.2;
  camera.position.set(0, 2.1, camDist);
  camera.lookAt(0, 1.35, 0);

  var renderer = new THREE.WebGLRenderer({ antialias: true, alpha: false, powerPreference: 'high-performance' });
  renderer.setSize(innerWidth, innerHeight);
  renderer.setPixelRatio(Math.min(devicePixelRatio, reduced ? 1 : 2));
  renderer.shadowMap.enabled = !reduced;
  if (renderer.shadowMap.enabled) renderer.shadowMap.type = THREE.PCFSoftShadowMap;
  if (THREE.ACESFilmicToneMapping) {
    renderer.toneMapping = THREE.ACESFilmicToneMapping;
    renderer.toneMappingExposure = 1.05;
  }
  wrap.appendChild(renderer.domElement);

  scene.add(new THREE.HemisphereLight(0xb8cce8, 0x1a1510, 0.55));

  var sun = new THREE.DirectionalLight(0xfff4e8, 1.85);
  sun.position.set(6, 14, 8);
  if (renderer.shadowMap.enabled) {
    sun.castShadow = true;
    sun.shadow.mapSize.set(2048, 2048);
    sun.shadow.bias = -0.00015;
    sun.shadow.camera.near = 1;
    sun.shadow.camera.far = 40;
    sun.shadow.camera.left = sun.shadow.camera.bottom = -12;
    sun.shadow.camera.right = sun.shadow.camera.top = 12;
  }
  scene.add(sun);

  var fill = new THREE.DirectionalLight(0x88aacc, 0.35);
  fill.position.set(-8, 6, 4);
  scene.add(fill);

  var rim = new THREE.DirectionalLight(0xffd8a8, 0.55);
  rim.position.set(0, 4, -10);
  scene.add(rim);

  function mat(color, rough, metal) {
    return new THREE.MeshStandardMaterial({
      color: color,
      roughness: rough != null ? rough : 0.42,
      metalness: metal != null ? metal : 0.04
    });
  }

  function glassMat() {
    return new THREE.MeshPhysicalMaterial({
      color: 0xd8e8f8,
      roughness: 0.04,
      metalness: 0,
      transmission: 0.82,
      thickness: 0.35,
      transparent: true,
      opacity: 0.92,
      ior: 1.48
    });
  }

  /* ── Paesaggio 3D ── */
  var env = new THREE.Group();

  var ground = new THREE.Mesh(
    new THREE.CircleGeometry(28, 64),
    mat(0x1a2420, 0.92, 0.02)
  );
  ground.rotation.x = -Math.PI / 2;
  ground.receiveShadow = true;
  env.add(ground);

  var lawn = new THREE.Mesh(
    new THREE.CircleGeometry(9, 48),
    mat(0x355040, 0.88, 0)
  );
  lawn.rotation.x = -Math.PI / 2;
  lawn.position.y = 0.01;
  lawn.receiveShadow = true;
  env.add(lawn);

  var podium = new THREE.Mesh(
    new THREE.CylinderGeometry(4.2, 4.4, 0.18, 48),
    mat(0x3a3632, 0.55, 0.08)
  );
  podium.position.y = 0.09;
  podium.receiveShadow = true;
  podium.castShadow = true;
  env.add(podium);

  function hill(x, z, r, h, color) {
    var m = new THREE.Mesh(
      new THREE.ConeGeometry(r, h, 8),
      mat(color, 0.95, 0)
    );
    m.position.set(x, h * 0.5 - 0.2, z);
    m.receiveShadow = true;
    env.add(m);
  }

  hill(-14, -16, 5.5, 3.2, 0x2a4538);
  hill(12, -18, 6, 3.8, 0x243a30);
  hill(-10, 14, 4.5, 2.6, 0x2d4a3c);
  hill(15, 10, 5, 3, 0x284035);

  function tree(x, z, scale) {
    var g = new THREE.Group();
    var trunk = new THREE.Mesh(
      new THREE.CylinderGeometry(0.12 * scale, 0.16 * scale, 0.9 * scale, 6),
      mat(0x3d2e22, 0.85, 0)
    );
    trunk.position.y = 0.45 * scale;
    trunk.castShadow = true;
    var crown = new THREE.Mesh(
      new THREE.ConeGeometry(0.65 * scale, 1.6 * scale, 7),
      mat(0x3a5c48, 0.82, 0)
    );
    crown.position.y = 1.35 * scale;
    crown.castShadow = true;
    g.add(trunk, crown);
    g.position.set(x, 0, z);
    env.add(g);
  }

  tree(-7.5, -5, 1.1);
  tree(8, -4.5, 0.95);
  tree(-6, 6, 0.85);
  tree(7.5, 5.5, 1);

  var path = new THREE.Mesh(
    new THREE.PlaneGeometry(1.4, 5),
    mat(0x4a443c, 0.78, 0.05)
  );
  path.rotation.x = -Math.PI / 2;
  path.position.set(0, 0.02, 4.2);
  path.receiveShadow = true;
  env.add(path);

  scene.add(env);

  /* ── Villa moderna (proporzioni architettoniche) ── */
  var house = new THREE.Group();
  house.position.y = 0.18;

  function box(w, h, d, material, x, y, z) {
    var m = new THREE.Mesh(new THREE.BoxGeometry(w, h, d), material);
    m.position.set(x, y, z);
    m.castShadow = true;
    m.receiveShadow = true;
    house.add(m);
    return m;
  }

  var white = mat(0xf0ebe4, 0.38);
  var dark = mat(0x2a2622, 0.35, 0.12);
  var wood = mat(0x6b4a32, 0.62, 0);
  var roof = mat(0x3a3836, 0.32, 0.15);
  var concrete = mat(0x8a8580, 0.68, 0.02);

  box(4.2, 0.22, 3.4, concrete, 0, 0.11, 0);

  box(3.6, 2.05, 2.85, white, 0, 1.25, 0);
  box(3.0, 1.55, 2.35, white, 0.15, 2.95, -0.05);
  box(3.8, 0.12, 3.05, roof, 0.1, 3.78, -0.05);

  box(0.55, 2.1, 2.9, wood, -1.52, 1.28, 0);
  box(0.08, 2.05, 2.85, dark, -1.22, 1.25, 0);

  box(0.75, 1.65, 0.1, dark, 0.55, 0.95, 1.48);
  box(1.05, 0.06, 0.55, dark, 0.55, 1.78, 1.55);

  function windowPane(w, h, x, y, z) {
    house.add(new THREE.Mesh(new THREE.PlaneGeometry(w, h), glassMat()).translateX(x).translateY(y).translateZ(z));
    var glow = new THREE.Mesh(
      new THREE.PlaneGeometry(w * 0.88, h * 0.88),
      new THREE.MeshBasicMaterial({ color: 0xffe8c8, transparent: true, opacity: 0.22 })
    );
    glow.position.set(x, y, z - 0.04);
    house.add(glow);
    box(0.04, h + 0.08, 0.04, dark, x, y, z - 0.02);
  }

  windowPane(1.55, 1.35, 0.05, 1.35, 1.46);
  windowPane(0.85, 0.95, -0.95, 1.25, 1.46);
  windowPane(0.85, 0.95, 1.05, 1.25, 1.46);
  windowPane(0.95, 0.75, 0.35, 2.85, 1.22);
  windowPane(0.65, 0.65, -0.55, 2.85, 1.22);

  function balcony(y, z, w) {
    box(w, 0.07, 0.75, concrete, 0.05, y, z);
    house.add(new THREE.Mesh(new THREE.PlaneGeometry(w, 0.48), glassMat()).translateX(0.05).translateY(y + 0.28).translateZ(z + 0.38));
    box(0.05, 0.48, 0.05, dark, -w / 2 + 0.12, y + 0.28, z + 0.38);
    box(0.05, 0.48, 0.05, dark, w / 2 - 0.12, y + 0.28, z + 0.38);
  }

  balcony(2.05, 1.48, 1.55);
  balcony(2.95, 1.25, 1.35);

  for (var i = 0; i < 3; i++) {
    box(1.2, 0.14, 0.55, concrete, 0, 0.07 + i * 0.14, 2.05 + i * 0.12);
  }

  box(1.15, 0.05, 0.72, mat(0x2a7a9a, 0.18, 0.08), -0.65, 0.24, 0.55);

  scene.add(house);

  /* ── Scroll → rotazione immediata ── */
  function maxScroll() {
    if (!layer) return 1;
    return Math.max(innerHeight * 3, layer.offsetHeight - innerHeight);
  }

  function progress() {
    return Math.min(1, Math.max(0, scrollY / maxScroll()));
  }

  function updateScene(p) {
    house.rotation.y = p * Math.PI * 2 * CFG.turns;
    if (bar) bar.style.width = (p * 100) + '%';
    if (hint && p > 0.005) hint.classList.add('hidden');
  }

  function onScroll() { updateScene(progress()); }

  function onResize() {
    mobile = matchMedia('(max-width:768px)').matches;
    camDist = mobile ? 11.5 : 9.2;
    camera.aspect = innerWidth / innerHeight;
    camera.updateProjectionMatrix();
    camera.position.set(0, 2.1, camDist);
    camera.lookAt(0, 1.35, 0);
    renderer.setSize(innerWidth, innerHeight);
    renderer.setPixelRatio(Math.min(devicePixelRatio, reduced ? 1 : 2));
  }

  var raf;
  function loop() {
    raf = requestAnimationFrame(loop);
    updateScene(progress());
    renderer.render(scene, camera);
  }

  addEventListener('scroll', onScroll, { passive: true });
  addEventListener('resize', onResize);

  if (loading) loading.classList.add('hidden');
  onScroll();
  onResize();
  loop();

  addEventListener('beforeunload', function () {
    cancelAnimationFrame(raf);
    renderer.dispose();
    scene.traverse(function (o) {
      if (o.geometry) o.geometry.dispose();
      if (o.material) {
        if (Array.isArray(o.material)) o.material.forEach(function (m) { m.dispose(); });
        else o.material.dispose();
      }
    });
  });
})();
