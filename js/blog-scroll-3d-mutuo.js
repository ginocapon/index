/**
 * Mutuo under 36 — showcase 3D (da zero)
 * Foto reale fissa · villa moderna trasparente · rotazione 1:1 collo scroll
 */
(function () {
  'use strict';

  var CFG = {
    turns: 3.5,
    texEnv: 'img/blog/blog-prima-casa-under-36-consap-hero.webp',
    texInterior: 'img/3d/mutuo-house-interior-ref.webp'
  };

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

  /* ── Renderer (canvas trasparente sopra la foto) ── */
  var scene = new THREE.Scene();
  var camera = new THREE.PerspectiveCamera(40, innerWidth / innerHeight, 0.08, 80);
  var dist = mobile ? 10.5 : 8.8;
  camera.position.set(0, 1.7, dist);
  camera.lookAt(0, 1.5, 0);

  var renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true, powerPreference: 'high-performance' });
  renderer.setSize(innerWidth, innerHeight);
  renderer.setPixelRatio(Math.min(devicePixelRatio, reduced ? 1 : 2.5));
  renderer.setClearColor(0x000000, 0);
  renderer.shadowMap.enabled = !reduced;
  if (renderer.shadowMap.enabled) renderer.shadowMap.type = THREE.PCFSoftShadowMap;
  if (THREE.ACESFilmicToneMapping) {
    renderer.toneMapping = THREE.ACESFilmicToneMapping;
    renderer.toneMappingExposure = 1.12;
  }
  wrap.appendChild(renderer.domElement);

  /* ── Luci (luce diurna morbida) ── */
  scene.add(new THREE.AmbientLight(0xfff6ee, 0.55));

  var sun = new THREE.DirectionalLight(0xfff0e0, 2.1);
  sun.position.set(5, 12, 7);
  if (renderer.shadowMap.enabled) {
    sun.castShadow = true;
    sun.shadow.mapSize.set(2048, 2048);
    sun.shadow.bias = -0.0002;
    sun.shadow.camera.near = 0.5;
    sun.shadow.camera.far = 35;
    sun.shadow.camera.left = sun.shadow.camera.bottom = -7;
    sun.shadow.camera.right = sun.shadow.camera.top = 7;
  }
  scene.add(sun);
  var fill = new THREE.DirectionalLight(0xc8d8f0, 0.5);
  fill.position.set(-6, 4, 4);
  scene.add(fill);
  var rim = new THREE.DirectionalLight(0xffe0b8, 0.75);
  rim.position.set(0, 3, -8);
  scene.add(rim);

  var loader = new THREE.TextureLoader();
  var interiorMap = null;
  var windowInners = [];

  loader.load(CFG.texInterior, function (t) {
    t.colorSpace = THREE.SRGBColorSpace;
    interiorMap = t;
    windowInners.forEach(function (m) {
      m.material.map = t;
      m.material.color.set(0xffffff);
      m.material.opacity = 0.68;
      m.material.needsUpdate = true;
    });
  });

  function mat(color, rough, metal) {
    return new THREE.MeshPhysicalMaterial({
      color: color,
      roughness: rough != null ? rough : 0.38,
      metalness: metal != null ? metal : 0.06,
      clearcoat: 0.15,
      clearcoatRoughness: 0.4
    });
  }

  function glass() {
    return new THREE.MeshPhysicalMaterial({
      color: 0xe8f2fa,
      roughness: 0.03,
      metalness: 0,
      transmission: 0.9,
      thickness: 0.4,
      transparent: true,
      clearcoat: 1,
      clearcoatRoughness: 0.05,
      ior: 1.45
    });
  }

  /* ── Ombra al suolo (integrata sulla foto) ── */
  var shadowDisc = new THREE.Mesh(
    new THREE.CircleGeometry(2.8, 48),
    new THREE.MeshBasicMaterial({ color: 0x000000, transparent: true, opacity: 0.38 })
  );
  shadowDisc.rotation.x = -Math.PI / 2;
  shadowDisc.position.y = 0.02;
  scene.add(shadowDisc);

  /* ── Villa moderna (condominio contemporaneo) ── */
  var villa = new THREE.Group();

  function box(w, h, d, material, x, y, z) {
    var m = new THREE.Mesh(new THREE.BoxGeometry(w, h, d), material);
    m.position.set(x, y, z);
    m.castShadow = true;
    m.receiveShadow = true;
    villa.add(m);
    return m;
  }

  box(3.6, 0.24, 2.8, mat(0xc4bcb4, 0.48), 0, 0.12, 0);

  box(3.1, 2.1, 2.2, mat(0xeae4dc, 0.4), 0, 1.35, 0);
  box(2.5, 1.2, 1.9, mat(0xf4f0ea, 0.35), 0.25, 2.95, -0.05);
  box(3.2, 0.1, 2.4, mat(0x454340, 0.28, 0.2), 0.15, 3.55, -0.05);

  box(0.14, 2.2, 2.15, mat(0x5c4838, 0.65), -1.55, 1.35, 0);

  function win(w, h, x, y, z) {
    villa.add(new THREE.Mesh(new THREE.PlaneGeometry(w, h), glass()).translateX(x).translateY(y).translateZ(z));
    var inner = new THREE.Mesh(
      new THREE.PlaneGeometry(w * 0.9, h * 0.9),
      new THREE.MeshBasicMaterial({ color: 0xfff4e8, transparent: true, opacity: 0.32 })
    );
    inner.position.set(x, y, z - 0.05);
    villa.add(inner);
    windowInners.push(inner);
  }

  win(1.4, 1.1, 0, 1.5, 1.12);
  win(0.9, 1, -0.9, 1.4, 1.12);
  win(0.9, 1, 0.9, 1.4, 1.12);
  win(1, 0.8, 0.4, 2.9, 0.98);
  win(0.7, 0.75, -0.5, 2.9, 0.98);

  function balcony(y, z, w) {
    box(w, 0.06, 0.7, mat(0xd0ccc6, 0.42), 0.1, y, z);
    box(w, 0.5, 0.025, glass(), 0.1, y + 0.28, z + 0.36);
    box(0.04, 0.5, 0.04, mat(0x3a322c, 0.4, 0.15), -w / 2 + 0.1, y + 0.28, z + 0.36);
    box(0.04, 0.5, 0.04, mat(0x3a322c, 0.4, 0.15), w / 2 - 0.1, y + 0.28, z + 0.36);
  }
  balcony(2.1, 1.15, 1.45);
  balcony(3.05, 0.92, 1.3);

  box(0.65, 1.5, 0.08, mat(0x2a2420, 0.42, 0.15), -0.5, 0.98, 1.13);
  box(1.1, 0.05, 0.5, mat(0x3a322c, 0.32, 0.2), -0.5, 1.75, 1.28);

  [[0, 1.5], [-0.9, 1.4], [0.9, 1.4]].forEach(function (p) {
    box(0.05, 1.15, 0.05, mat(0x3a322c, 0.45, 0.12), p[0], p[1], 1.14);
  });

  box(1.2, 0.04, 0.75, mat(0x3a8aaa, 0.15, 0.1), -0.7, 0.22, 0.45);

  scene.add(villa);

  /* ── Scroll → rotazione immediata ── */
  function maxScroll() {
    if (!layer) return 1;
    return Math.max(innerHeight * 3, layer.offsetHeight - innerHeight);
  }

  function progress() {
    return Math.min(1, Math.max(0, scrollY / maxScroll()));
  }

  function updateScene(p) {
    villa.rotation.y = p * Math.PI * 2 * CFG.turns;
    villa.position.x = mobile ? p * 1.1 : p * 0.2;
    if (bar) bar.style.width = (p * 100) + '%';
    if (hint && p > 0.005) hint.classList.add('hidden');
  }

  function onScroll() { updateScene(progress()); }

  function onResize() {
    mobile = matchMedia('(max-width:768px)').matches;
    dist = mobile ? 10.5 : 8.8;
    camera.aspect = innerWidth / innerHeight;
    camera.updateProjectionMatrix();
    camera.position.set(0, 1.7, dist);
    camera.lookAt(0, 1.5, 0);
    renderer.setSize(innerWidth, innerHeight);
    renderer.setPixelRatio(Math.min(devicePixelRatio, reduced ? 1 : 2.5));
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
