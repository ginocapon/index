/**
 * Scroll 3D showcase — mutuo under 36
 * Casa moderna premium · rotazione 1:1 immediata con lo scroll
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
  scene.background = new THREE.Color(0x121110);
  scene.fog = new THREE.FogExp2(0x121110, 0.028);

  var camera = new THREE.PerspectiveCamera(48, window.innerWidth / window.innerHeight, 0.1, 120);
  var camDist = isMobile ? 10.5 : 8.6;
  camera.position.set(0, 1.55, camDist);
  camera.lookAt(0, 1.25, 0);

  var renderer = new THREE.WebGLRenderer({ antialias: true, alpha: false, powerPreference: 'high-performance' });
  renderer.setSize(window.innerWidth, window.innerHeight);
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, reducedMotion ? 1 : 2.25));
  renderer.shadowMap.enabled = !reducedMotion;
  if (renderer.shadowMap.enabled) renderer.shadowMap.type = THREE.PCFSoftShadowMap;
  if (THREE.ACESFilmicToneMapping) {
    renderer.toneMapping = THREE.ACESFilmicToneMapping;
    renderer.toneMappingExposure = 1.08;
  }
  wrap.appendChild(renderer.domElement);

  scene.add(new THREE.AmbientLight(0xfff8f0, 0.42));

  var keyLight = new THREE.DirectionalLight(0xfff5eb, 2.2);
  keyLight.position.set(5, 12, 7);
  if (renderer.shadowMap.enabled) {
    keyLight.castShadow = true;
    keyLight.shadow.mapSize.set(2048, 2048);
    keyLight.shadow.bias = -0.00015;
  }
  scene.add(keyLight);

  var fillLight = new THREE.DirectionalLight(0xc8d4e8, 0.55);
  fillLight.position.set(-6, 4, 5);
  scene.add(fillLight);

  var rimLight = new THREE.DirectionalLight(0xd4af6a, 1.35);
  rimLight.position.set(0, 5, -9);
  scene.add(rimLight);

  var spotGold = new THREE.PointLight(0xd4af6a, 1.1, 28);
  spotGold.position.set(2.5, 5, 3);
  scene.add(spotGold);

  var spotCool = new THREE.PointLight(0x8eb4ff, 0.75, 24);
  spotCool.position.set(-3, 3, 2);
  scene.add(spotCool);

  var accentBlue = new THREE.PointLight(0x5a9fd4, 0.5, 20);
  accentBlue.position.set(-3.5, 2.5, 1);
  scene.add(accentBlue);

  var accentOrange = new THREE.PointLight(0xff7a45, 0.45, 20);
  accentOrange.position.set(3.5, 2.5, 1);
  scene.add(accentOrange);

  function stdMat(color, metal, rough, emissive, emInt) {
    var opts = {
      color: color,
      metalness: metal != null ? metal : 0.35,
      roughness: rough != null ? rough : 0.28
    };
    if (emissive) {
      opts.emissive = new THREE.Color(emissive);
      opts.emissiveIntensity = emInt != null ? emInt : 0.15;
    }
    return new THREE.MeshStandardMaterial(opts);
  }

  function glassMat() {
    return stdMat(0x1a2838, 0.92, 0.06, 0x6a9fd4, 0.22);
  }

  /* ── Ambiente showroom elitario ── */
  var env = new THREE.Group();

  var floorMain = new THREE.Mesh(
    new THREE.CircleGeometry(9, 96),
    stdMat(0x1c1a18, 0.55, 0.18)
  );
  floorMain.rotation.x = -Math.PI / 2;
  floorMain.receiveShadow = true;
  env.add(floorMain);

  for (var ri = 1; ri <= 4; ri++) {
    var ringFloor = new THREE.Mesh(
      new THREE.RingGeometry(ri * 1.35, ri * 1.35 + 0.018, 96),
      stdMat(0xd4af6a, 0.75, 0.22, 0xd4af6a, 0.08)
    );
    ringFloor.rotation.x = -Math.PI / 2;
    ringFloor.position.y = 0.004;
    env.add(ringFloor);
  }

  var backdrop = new THREE.Mesh(
    new THREE.CylinderGeometry(11, 11, 8, 64, 1, true, 0, Math.PI),
    stdMat(0x181614, 0.12, 0.88)
  );
  backdrop.position.set(0, 4, -5.5);
  env.add(backdrop);

  var ledStrip = new THREE.Mesh(
    new THREE.TorusGeometry(7.2, 0.012, 8, 128),
    stdMat(0xd4af6a, 0.2, 0.4, 0xffd98a, 0.85)
  );
  ledStrip.rotation.x = Math.PI / 2;
  ledStrip.position.y = 0.02;
  env.add(ledStrip);

  [[-5.5, -3], [5.5, -3], [-5.5, 3], [5.5, 3]].forEach(function (pos) {
    var pillar = new THREE.Mesh(
      new THREE.BoxGeometry(0.14, 5.5, 0.14),
      stdMat(0x2a2826, 0.65, 0.22)
    );
    pillar.position.set(pos[0], 2.75, pos[1]);
    pillar.castShadow = true;
    env.add(pillar);
  });

  scene.add(env);

  /* ── Pedestal marmo lucido ── */
  var pedestal = new THREE.Group();
  var pedBase = new THREE.Mesh(
    new THREE.CylinderGeometry(2.45, 2.65, 0.22, 64),
    stdMat(0x2e2c2a, 0.62, 0.14)
  );
  pedBase.position.y = 0.11;
  pedBase.receiveShadow = true;
  pedBase.castShadow = true;
  pedestal.add(pedBase);

  var pedTop = new THREE.Mesh(
    new THREE.CylinderGeometry(1.95, 2.05, 0.1, 64),
    stdMat(0xf0ece6, 0.48, 0.12)
  );
  pedTop.position.y = 0.27;
  pedestal.add(pedTop);

  var pedRing = new THREE.Mesh(
    new THREE.TorusGeometry(2.05, 0.022, 12, 96),
    stdMat(0xd4af6a, 0.88, 0.15, 0xffe0a0, 0.35)
  );
  pedRing.rotation.x = Math.PI / 2;
  pedRing.position.y = 0.33;
  pedestal.add(pedRing);
  scene.add(pedestal);

  /* ── Villa moderna HD (flat roof, vetrate, cantilever) ── */
  var house = new THREE.Group();
  house.position.set(0, 0.33, 0);
  house.rotation.z = -0.08;

  var baseSlab = new THREE.Mesh(
    new THREE.BoxGeometry(3.4, 0.14, 2.6),
    stdMat(0xe8e4de, 0.15, 0.55)
  );
  baseSlab.position.y = 0.07;
  baseSlab.castShadow = true;
  house.add(baseSlab);

  var mainVol = new THREE.Mesh(
    new THREE.BoxGeometry(2.85, 1.55, 2.15),
    stdMat(0xf7f5f1, 0.08, 0.38)
  );
  mainVol.position.set(0, 0.92, 0);
  mainVol.castShadow = true;
  mainVol.receiveShadow = true;
  house.add(mainVol);

  var upperVol = new THREE.Mesh(
    new THREE.BoxGeometry(2.35, 1.05, 1.85),
    stdMat(0xffffff, 0.06, 0.32)
  );
  upperVol.position.set(0.28, 2.22, -0.08);
  upperVol.castShadow = true;
  house.add(upperVol);

  var roofSlab = new THREE.Mesh(
    new THREE.BoxGeometry(3.15, 0.1, 2.45),
    stdMat(0x3a3836, 0.35, 0.42)
  );
  roofSlab.position.set(0.12, 2.82, -0.05);
  roofSlab.castShadow = true;
  house.add(roofSlab);

  var woodAccent = new THREE.Mesh(
    new THREE.BoxGeometry(0.35, 2.2, 2.18),
    stdMat(0x6b4f3a, 0.05, 0.72)
  );
  woodAccent.position.set(-1.38, 1.15, 0);
  house.add(woodAccent);

  var gMat = glassMat();
  [[0, 0.85, 1.09, 2.1, 1.35], [0.55, 2.15, 0.94, 1.05, 0.95], [-0.55, 2.15, 0.94, 1.05, 0.95]].forEach(function (g) {
    var glass = new THREE.Mesh(new THREE.BoxGeometry(g[3], g[4], 0.06), gMat);
    glass.position.set(g[0], g[1], g[2]);
    house.add(glass);
  });

  var door = new THREE.Mesh(
    new THREE.BoxGeometry(0.62, 1.35, 0.08),
    stdMat(0x1a1816, 0.55, 0.35)
  );
  door.position.set(0.95, 0.72, 1.1);
  house.add(door);

  var pool = new THREE.Mesh(
    new THREE.BoxGeometry(1.4, 0.05, 0.85),
    stdMat(0x2a6a8a, 0.65, 0.08, 0x4a9fd4, 0.35)
  );
  pool.position.set(-0.85, 0.16, 0.55);
  house.add(pool);

  var terrace = new THREE.Mesh(
    new THREE.BoxGeometry(1.1, 0.06, 0.7),
    stdMat(0xd8d4ce, 0.2, 0.45)
  );
  terrace.position.set(1.05, 1.58, 0.35);
  house.add(terrace);

  var railL = new THREE.Mesh(new THREE.BoxGeometry(0.03, 0.35, 0.7), stdMat(0xd4af6a, 0.82, 0.18));
  railL.position.set(0.58, 1.78, 0.35);
  house.add(railL);

  var railR = new THREE.Mesh(new THREE.BoxGeometry(0.03, 0.35, 0.7), stdMat(0xd4af6a, 0.82, 0.18));
  railR.position.set(1.52, 1.78, 0.35);
  house.add(railR);

  scene.add(house);

  var ROTATION_TURNS = 3.5;

  function scrollMax() {
    if (!scrollLayer) return 1;
    return Math.max(window.innerHeight * 3, scrollLayer.offsetHeight - window.innerHeight);
  }

  function scrollProgress() {
    return Math.min(1, Math.max(0, window.scrollY / scrollMax()));
  }

  function onScroll() {
    var p = scrollProgress();
    if (progressEl) progressEl.style.width = (p * 100) + '%';
    if (hintEl && p > 0.01) hintEl.classList.add('hidden');

    /* Rotazione immediata — nessun lerp, nessun ease */
    house.rotation.y = p * Math.PI * 2 * ROTATION_TURNS;

    var slideX = isMobile ? p * 1.2 : p * 0.28;
    house.position.x = slideX;

    if (maskEl) {
      maskEl.style.opacity = String(Math.max(0, 1 - p * 8));
    }

    accentBlue.intensity = 0.35 + (p > 0.32 && p < 0.52 ? 0.65 : 0.08);
    accentOrange.intensity = 0.3 + (p > 0.52 && p < 0.72 ? 0.7 : 0.06);
    spotGold.intensity = 0.85 + (p > 0.75 ? 0.55 : 0.15);
  }

  var animId;
  function animate() {
    animId = requestAnimationFrame(animate);
    var p = scrollProgress();
    house.rotation.y = p * Math.PI * 2 * ROTATION_TURNS;
    house.position.x = isMobile ? p * 1.2 : p * 0.28;
    rimLight.intensity = 1.1 + Math.sin(p * Math.PI * 2) * 0.2;
    renderer.render(scene, camera);
  }

  function onResize() {
    isMobile = window.matchMedia('(max-width: 768px)').matches;
    camDist = isMobile ? 10.5 : 8.6;
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    camera.position.set(0, 1.55, camDist);
    camera.lookAt(0, 1.25, 0);
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, reducedMotion ? 1 : 2.25));
  }

  if (maskEl) {
    maskEl.style.clipPath = 'circle(150% at 50% 50%)';
    maskEl.style.opacity = '0';
  }

  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('resize', onResize);

  if (loadingEl) loadingEl.classList.add('hidden');
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
