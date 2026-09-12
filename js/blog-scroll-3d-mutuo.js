/**
 * Scroll 3D showcase — mutuo under 36
 * Casa centrale che ruota con lo scroll (effetto product showcase, no camera fly-through)
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
  scene.background = new THREE.Color(0x0d1117);

  var camera = new THREE.PerspectiveCamera(52, window.innerWidth / window.innerHeight, 0.1, 100);
  var camDist = isMobile ? 9.2 : 7.4;
  camera.position.set(0, 1.35, camDist);
  camera.lookAt(0, 1.05, 0);

  var renderer = new THREE.WebGLRenderer({ antialias: true, alpha: false, powerPreference: 'high-performance' });
  renderer.setSize(window.innerWidth, window.innerHeight);
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, reducedMotion ? 1 : 2));
  renderer.shadowMap.enabled = !reducedMotion;
  if (renderer.shadowMap.enabled) renderer.shadowMap.type = THREE.PCFSoftShadowMap;
  wrap.appendChild(renderer.domElement);

  scene.add(new THREE.AmbientLight(0xffffff, 0.55));

  var keyLight = new THREE.DirectionalLight(0xffffff, 1.4);
  keyLight.position.set(4, 8, 6);
  if (renderer.shadowMap.enabled) {
    keyLight.castShadow = true;
    keyLight.shadow.mapSize.set(1024, 1024);
  }
  scene.add(keyLight);

  var fillLight = new THREE.DirectionalLight(0xffffff, 0.65);
  fillLight.position.set(-5, 2, 4);
  scene.add(fillLight);

  var rimLight = new THREE.DirectionalLight(0x4488cc, 1.1);
  rimLight.position.set(0, 3, -8);
  scene.add(rimLight);

  var accentBlue = new THREE.PointLight(0x4a90d9, 0.55, 18);
  accentBlue.position.set(-3, 3, 2);
  scene.add(accentBlue);

  var accentOrange = new THREE.PointLight(0xff6b35, 0.5, 18);
  accentOrange.position.set(3, 2, 2);
  scene.add(accentOrange);

  var accentGold = new THREE.PointLight(0xc9a84c, 0.45, 16);
  accentGold.position.set(0, 4, -2);
  scene.add(accentGold);

  function mat(color, metal, rough) {
    return new THREE.MeshStandardMaterial({
      color: color,
      metalness: metal != null ? metal : 0.22,
      roughness: rough != null ? rough : 0.58
    });
  }

  /* Pedestal */
  var pedestal = new THREE.Group();
  var pedBase = new THREE.Mesh(new THREE.CylinderGeometry(2.1, 2.35, 0.18, 48), mat(0x1a2744, 0.15, 0.82));
  pedBase.position.y = 0.09;
  pedBase.receiveShadow = true;
  pedestal.add(pedBase);
  var pedTop = new THREE.Mesh(new THREE.CylinderGeometry(1.65, 1.75, 0.12, 48), mat(0x243552, 0.2, 0.75));
  pedTop.position.y = 0.24;
  pedestal.add(pedTop);
  var ring = new THREE.Mesh(new THREE.TorusGeometry(1.85, 0.04, 8, 64), mat(0xc9a84c, 0.45, 0.35));
  ring.rotation.x = Math.PI / 2;
  ring.position.y = 0.31;
  pedestal.add(ring);
  scene.add(pedestal);

  /* Casa showcase — gruppo centrato, ruota con lo scroll */
  var house = new THREE.Group();
  house.position.set(0, 0.32, 0);
  house.rotation.z = -0.14;

  var body = new THREE.Mesh(new THREE.BoxGeometry(2.6, 1.85, 2.1), mat(0x2C4A6E, 0.18, 0.68));
  body.position.y = 1.12;
  body.castShadow = true;
  body.receiveShadow = true;
  house.add(body);

  var roof = new THREE.Mesh(new THREE.ConeGeometry(2.05, 1.25, 4), mat(0xc9a84c, 0.38, 0.42));
  roof.position.y = 2.55;
  roof.rotation.y = Math.PI / 4;
  roof.castShadow = true;
  house.add(roof);

  var chimney = new THREE.Mesh(new THREE.BoxGeometry(0.28, 0.65, 0.28), mat(0x4a5568, 0.2, 0.7));
  chimney.position.set(0.75, 2.85, -0.35);
  house.add(chimney);

  var door = new THREE.Mesh(new THREE.BoxGeometry(0.52, 0.95, 0.1), mat(0x152435, 0.1, 0.85));
  door.position.set(0, 0.72, 1.08);
  house.add(door);

  var winMat = mat(0x7ec8ff, 0.55, 0.22);
  [[-0.72, 1.35], [0.72, 1.35], [-0.72, 0.55], [0.72, 0.55]].forEach(function (w) {
    var win = new THREE.Mesh(new THREE.BoxGeometry(0.48, 0.48, 0.08), winMat);
    win.position.set(w[0], w[1], 1.06);
    house.add(win);
  });

  var step = new THREE.Mesh(new THREE.BoxGeometry(1.1, 0.12, 0.55), mat(0x3a4a62, 0.12, 0.8));
  step.position.set(0, 0.18, 1.15);
  house.add(step);

  /* Chiavi orbitanti */
  var keys = new THREE.Group();
  keys.position.set(0, 1.1, 0);
  var keyRing = new THREE.Mesh(new THREE.TorusGeometry(0.2, 0.035, 10, 28), mat(0xe8c96a, 0.58, 0.32));
  keyRing.rotation.x = Math.PI / 2;
  keyRing.position.set(1.55, 0.35, 0);
  keys.add(keyRing);
  var keyShaft = new THREE.Mesh(new THREE.BoxGeometry(0.07, 0.48, 0.07), mat(0xe8c96a, 0.52, 0.38));
  keyShaft.position.set(1.88, 0.1, 0);
  keys.add(keyShaft);
  house.add(keys);

  scene.add(house);

  /* Badge FISSO / VARIABILE che ruotano con la casa (faccette) */
  var badgeFisso = new THREE.Mesh(
    new THREE.BoxGeometry(0.02, 0.55, 0.9),
    mat(0x4a90d9, 0.3, 0.45)
  );
  badgeFisso.position.set(-1.32, 1.5, 0);
  house.add(badgeFisso);

  var badgeVar = new THREE.Mesh(
    new THREE.BoxGeometry(0.02, 0.55, 0.9),
    mat(0xff6b35, 0.3, 0.45)
  );
  badgeVar.position.set(1.32, 1.5, 0);
  house.add(badgeVar);

  var floor = new THREE.Mesh(new THREE.CircleGeometry(6, 48), mat(0x0f1a2e, 0.05, 0.95));
  floor.rotation.x = -Math.PI / 2;
  floor.position.y = 0;
  floor.receiveShadow = true;
  scene.add(floor);

  var targetProgress = 0;
  var smoothProgress = 0;

  function scrollMax() {
    if (!scrollLayer) return 1;
    return Math.max(window.innerHeight * 4, scrollLayer.offsetHeight - window.innerHeight);
  }

  function onScroll() {
    var max = scrollMax();
    targetProgress = Math.min(1, Math.max(0, window.scrollY / max));
    if (progressEl) progressEl.style.width = (targetProgress * 100) + '%';
    if (hintEl && targetProgress > 0.04) hintEl.classList.add('hidden');
  }

  function lerp(a, b, t) { return a + (b - a) * t; }
  function ease(t) { return t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2; }

  var animId;
  function animate() {
    animId = requestAnimationFrame(animate);
    smoothProgress = lerp(smoothProgress, targetProgress, reducedMotion ? 1 : 0.09);
    var p = ease(smoothProgress);

    /* Rotazione principale — 2 giri completi come la bottiglia nel demo */
    house.rotation.y = p * Math.PI * 4;

    /* Mobile: casa scivola a destra mentre ruota */
    var slideX = isMobile ? lerp(0, 1.35, Math.min(1, p * 1.4)) : lerp(0, 0.35, Math.sin(p * Math.PI));
    house.position.x = slideX;

    /* Leggero bob verticale */
    house.position.y = 0.32 + Math.sin(p * Math.PI * 2) * 0.06;

    keys.rotation.y = -p * Math.PI * 6;

    /* Maschera circolare che si apre all'inizio dello scroll */
    if (maskEl) {
      var maskR = lerp(0, 150, Math.min(1, p * 2.2));
      maskEl.style.clipPath = 'circle(' + maskR + '% at 50% 50%)';
      maskEl.style.opacity = String(lerp(1, 0, Math.min(1, (p - 0.15) * 3)));
    }

    /* Luci per sezione narrativa */
    accentBlue.intensity = 0.35 + (p > 0.35 && p < 0.55 ? 0.55 : 0.1);
    accentOrange.intensity = 0.3 + (p > 0.55 && p < 0.75 ? 0.6 : 0.08);
    accentGold.intensity = 0.25 + (p > 0.78 ? 0.55 : 0.05);
    rimLight.intensity = 0.85 + Math.sin(p * Math.PI) * 0.35;

    renderer.render(scene, camera);
  }

  function onResize() {
    isMobile = window.matchMedia('(max-width: 768px)').matches;
    camDist = isMobile ? 9.2 : 7.4;
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    camera.position.set(0, 1.35, camDist);
    camera.lookAt(0, 1.05, 0);
    renderer.setSize(window.innerWidth, window.innerHeight);
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
