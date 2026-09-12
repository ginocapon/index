/**
 * Mutuo under 36 — showcase fotorealistico
 * Sfondo foto reale · villa moderna 3D PBR · rotazione istantanea allo scroll
 */
(function () {
  'use strict';

  var reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var isMobile = window.matchMedia('(max-width: 768px)').matches;
  var wrap = document.getElementById('b3d-canvas-wrap');
  var loadingEl = document.querySelector('.b3d-loading');
  var hintEl = document.querySelector('.b3d-scroll-hint');
  var progressEl = document.querySelector('.b3d-progress');
  var scrollLayer = document.querySelector('.b3d-scroll-layer');
  var maskEl = document.querySelector('.b3d-showcase-mask');

  if (!wrap || typeof THREE === 'undefined') {
    if (loadingEl) loadingEl.textContent = 'Scena 3D non disponibile';
    return;
  }

  var scene = new THREE.Scene();

  var camera = new THREE.PerspectiveCamera(42, window.innerWidth / window.innerHeight, 0.1, 120);
  var camDist = isMobile ? 11 : 9;
  camera.position.set(0, 1.65, camDist);
  camera.lookAt(0, 1.45, 0);

  var renderer = new THREE.WebGLRenderer({ antialias: true, alpha: false, powerPreference: 'high-performance' });
  renderer.setSize(window.innerWidth, window.innerHeight);
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, reducedMotion ? 1 : 2.5));
  renderer.shadowMap.enabled = !reducedMotion;
  if (renderer.shadowMap.enabled) renderer.shadowMap.type = THREE.PCFSoftShadowMap;
  if (THREE.ACESFilmicToneMapping) {
    renderer.toneMapping = THREE.ACESFilmicToneMapping;
    renderer.toneMappingExposure = 1.05;
  }
  wrap.appendChild(renderer.domElement);

  var texLoader = new THREE.TextureLoader();
  var interiorTex = null;
  var windowGlows = [];

  texLoader.load('img/3d/mutuo-showcase-env.webp', function (envTex) {
    envTex.colorSpace = THREE.SRGBColorSpace;
    scene.background = envTex;
    if (loadingEl) loadingEl.classList.add('hidden');
  }, undefined, function () {
    scene.background = new THREE.Color(0x1a1816);
    if (loadingEl) loadingEl.classList.add('hidden');
  });

  texLoader.load('img/3d/mutuo-house-interior-ref.webp', function (t) {
    t.colorSpace = THREE.SRGBColorSpace;
    interiorTex = t;
    windowGlows.forEach(function (g) {
      g.material.map = t;
      g.material.needsUpdate = true;
    });
  });

  scene.add(new THREE.AmbientLight(0xfff8f2, 0.45));

  var sun = new THREE.DirectionalLight(0xfff4ea, 1.85);
  sun.position.set(6, 14, 8);
  if (renderer.shadowMap.enabled) {
    sun.castShadow = true;
    sun.shadow.mapSize.set(2048, 2048);
    sun.shadow.camera.near = 1;
    sun.shadow.camera.far = 40;
    sun.shadow.camera.left = -8;
    sun.shadow.camera.right = 8;
    sun.shadow.camera.top = 8;
    sun.shadow.camera.bottom = -8;
  }
  scene.add(sun);

  var fill = new THREE.DirectionalLight(0xd8e8ff, 0.45);
  fill.position.set(-7, 5, 4);
  scene.add(fill);

  var rim = new THREE.DirectionalLight(0xffe8c8, 0.9);
  rim.position.set(0, 4, -10);
  scene.add(rim);

  function phys(color, rough, metal, emissive, emInt) {
    var m = new THREE.MeshPhysicalMaterial({
      color: color,
      roughness: rough != null ? rough : 0.35,
      metalness: metal != null ? metal : 0.08,
      envMapIntensity: 0.55
    });
    if (emissive) {
      m.emissive = new THREE.Color(emissive);
      m.emissiveIntensity = emInt != null ? emInt : 0.2;
    }
    return m;
  }

  function glassMat() {
    return new THREE.MeshPhysicalMaterial({
      color: 0xdce8f5,
      metalness: 0,
      roughness: 0.04,
      transmission: 0.88,
      thickness: 0.35,
      transparent: true,
      envMapIntensity: 0.9,
      clearcoat: 1,
      clearcoatRoughness: 0.08
    });
  }

  /* Piano ombre sotto la villa */
  var ground = new THREE.Mesh(
    new THREE.CircleGeometry(5.5, 64),
    phys(0x1a1816, 0.85, 0.05)
  );
  ground.rotation.x = -Math.PI / 2;
  ground.position.y = 0.001;
  ground.receiveShadow = true;
  scene.add(ground);

  var house = new THREE.Group();
  house.position.set(0, 0, 0);

  /* Podio in pietra chiara */
  var podium = new THREE.Mesh(new THREE.BoxGeometry(3.8, 0.28, 2.9), phys(0xc8c0b8, 0.55, 0.05));
  podium.position.y = 0.14;
  podium.castShadow = true;
  podium.receiveShadow = true;
  house.add(podium);

  /* Corpo principale — stucco moderno beige (come edificio foto hero) */
  var main = new THREE.Mesh(new THREE.BoxGeometry(3.2, 2.05, 2.35), phys(0xe8e0d4, 0.42, 0.04));
  main.position.y = 1.34;
  main.castShadow = true;
  main.receiveShadow = true;
  house.add(main);

  /* Piano superiore cantilever */
  var upper = new THREE.Mesh(new THREE.BoxGeometry(2.55, 1.15, 2.05), phys(0xf2ece4, 0.38, 0.04));
  upper.position.set(0.22, 2.88, -0.05);
  upper.castShadow = true;
  house.add(upper);

  /* Attico / parapetto */
  var roofSlab = new THREE.Mesh(new THREE.BoxGeometry(3.35, 0.12, 2.55), phys(0x4a4846, 0.32, 0.25));
  roofSlab.position.set(0.1, 3.52, -0.05);
  roofSlab.castShadow = true;
  house.add(roofSlab);

  /* Vetrate panoramiche */
  function addWindow(w, h, x, y, z) {
    var g = new THREE.Mesh(new THREE.PlaneGeometry(w, h), glassMat());
    g.position.set(x, y, z);
    house.add(g);
    var glow = new THREE.Mesh(
      new THREE.PlaneGeometry(w * 0.92, h * 0.92),
      new THREE.MeshBasicMaterial({
        map: interiorTex || null,
        color: interiorTex ? 0xffffff : 0xfff0dc,
        transparent: true,
        opacity: interiorTex ? 0.62 : 0.35
      })
    );
    glow.position.set(x, y, z - 0.04);
    house.add(glow);
    windowGlows.push(glow);
  }

  addWindow(1.35, 1.05, 0, 1.45, 1.19);
  addWindow(0.85, 0.95, -0.95, 1.35, 1.19);
  addWindow(0.85, 0.95, 0.95, 1.35, 1.19);
  addWindow(1.05, 0.75, 0.35, 2.85, 1.04);
  addWindow(0.75, 0.75, -0.55, 2.85, 1.04);

  /* Balconi con ringhiere vetro */
  function addBalcony(y, z, w) {
    var slab = new THREE.Mesh(new THREE.BoxGeometry(w, 0.07, 0.75), phys(0xd8d4ce, 0.45, 0.1));
    slab.position.set(0.15, y, z);
    slab.castShadow = true;
    house.add(slab);
    var rail = new THREE.Mesh(new THREE.BoxGeometry(w, 0.55, 0.03), glassMat());
    rail.position.set(0.15, y + 0.3, z + 0.38);
    house.add(rail);
  }
  addBalcony(2.05, 1.22, 1.5);
  addBalcony(3.05, 0.98, 1.35);

  /* Telaio scuro finestre */
  [[0, 1.45], [-0.95, 1.35], [0.95, 1.35]].forEach(function (p) {
    var frame = new THREE.Mesh(new THREE.BoxGeometry(0.06, 1.1, 0.06), phys(0x3d3028, 0.5, 0.15));
    frame.position.set(p[0], p[1], 1.2);
    house.add(frame);
  });

  /* Portoncino ingresso */
  var entry = new THREE.Mesh(new THREE.BoxGeometry(0.72, 1.45, 0.1), phys(0x2a2420, 0.45, 0.2));
  entry.position.set(-0.55, 0.95, 1.2);
  house.add(entry);

  var canopy = new THREE.Mesh(new THREE.BoxGeometry(1.15, 0.05, 0.55), phys(0x3d3028, 0.35, 0.3));
  canopy.position.set(-0.55, 1.72, 1.35);
  house.add(canopy);

  /* Accento legno / brise-soleil */
  var brise = new THREE.Mesh(new THREE.BoxGeometry(0.12, 1.8, 2.1), phys(0x6b5344, 0.62, 0.05));
  brise.position.set(-1.62, 1.35, 0);
  house.add(brise);

  scene.add(house);

  var ROTATION_TURNS = 3.5;

  function scrollMax() {
    if (!scrollLayer) return 1;
    return Math.max(window.innerHeight * 3, scrollLayer.offsetHeight - window.innerHeight);
  }

  function scrollProgress() {
    return Math.min(1, Math.max(0, window.scrollY / scrollMax()));
  }

  function applyScroll(p) {
    house.rotation.y = p * Math.PI * 2 * ROTATION_TURNS;
    house.position.x = isMobile ? p * 1.15 : p * 0.22;
    if (progressEl) progressEl.style.width = (p * 100) + '%';
    if (hintEl && p > 0.008) hintEl.classList.add('hidden');
    if (maskEl) maskEl.style.opacity = '0';
  }

  function onScroll() {
    applyScroll(scrollProgress());
  }

  var animId;
  function animate() {
    animId = requestAnimationFrame(animate);
    applyScroll(scrollProgress());
    renderer.render(scene, camera);
  }

  function onResize() {
    isMobile = window.matchMedia('(max-width: 768px)').matches;
    camDist = isMobile ? 11 : 9;
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    camera.position.set(0, 1.65, camDist);
    camera.lookAt(0, 1.45, 0);
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, reducedMotion ? 1 : 2.5));
  }

  if (maskEl) maskEl.style.opacity = '0';

  wrap.style.backgroundImage = "url('img/3d/mutuo-showcase-env.webp')";
  wrap.style.backgroundSize = 'cover';
  wrap.style.backgroundPosition = 'center';

  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('resize', onResize);

  onScroll();
  onResize();
  animate();

  window.addEventListener('beforeunload', function () {
    cancelAnimationFrame(animId);
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
