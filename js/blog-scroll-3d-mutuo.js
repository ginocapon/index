/**
 * Scroll 3D — mutuo under 36, tassi fisso vs variabile
 * Three.js locale · camera guidata dallo scroll
 */
(function () {
  'use strict';

  var reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var wrap = document.getElementById('b3d-canvas-wrap');
  var loadingEl = document.querySelector('.b3d-loading');
  var hintEl = document.querySelector('.b3d-scroll-hint');
  var progressEl = document.querySelector('.b3d-progress');
  var scrollLayer = document.querySelector('.b3d-scroll-layer');

  if (!wrap || typeof THREE === 'undefined') {
    if (loadingEl) loadingEl.textContent = 'Scena 3D non disponibile';
    return;
  }

  var scene = new THREE.Scene();
  scene.background = new THREE.Color(0x0f1a2e);
  scene.fog = new THREE.Fog(0x0f1a2e, 10, 52);

  var camera = new THREE.PerspectiveCamera(68, window.innerWidth / window.innerHeight, 0.1, 120);
  camera.position.set(0, 2.4, 16);

  var renderer = new THREE.WebGLRenderer({ antialias: true, alpha: false, powerPreference: 'high-performance' });
  renderer.setSize(window.innerWidth, window.innerHeight);
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, reducedMotion ? 1 : 1.75));
  renderer.shadowMap.enabled = !reducedMotion;
  if (renderer.shadowMap.enabled) renderer.shadowMap.type = THREE.PCFSoftShadowMap;
  wrap.appendChild(renderer.domElement);

  scene.add(new THREE.AmbientLight(0xffffff, 0.38));

  var sun = new THREE.DirectionalLight(0xffeedd, 0.9);
  sun.position.set(5, 12, 8);
  if (renderer.shadowMap.enabled) { sun.castShadow = true; sun.shadow.mapSize.set(1024, 1024); }
  scene.add(sun);

  var blueLight = new THREE.PointLight(0x4a90d9, 0.5, 24);
  blueLight.position.set(-4, 4, -6);
  scene.add(blueLight);

  var orangeLight = new THREE.PointLight(0xff6b35, 0.45, 24);
  orangeLight.position.set(4, 3, -18);
  scene.add(orangeLight);

  function mat(color, metal, rough) {
    return new THREE.MeshStandardMaterial({ color: color, metalness: metal || 0.2, roughness: rough || 0.6 });
  }

  var floor = new THREE.Mesh(new THREE.PlaneGeometry(16, 65), mat(0x152435, 0.08, 0.88));
  floor.rotation.x = -Math.PI / 2;
  floor.position.set(0, 0, -16);
  floor.receiveShadow = true;
  scene.add(floor);

  /* Mini casa + chiavi */
  var home = new THREE.Group();
  home.position.set(0, 0, -2);
  var body = new THREE.Mesh(new THREE.BoxGeometry(2.2, 1.6, 1.8), mat(0x2C4A6E, 0.15, 0.7));
  body.position.y = 0.8;
  body.castShadow = true;
  home.add(body);
  var roof = new THREE.Mesh(new THREE.ConeGeometry(1.7, 1, 4), mat(0xc9a84c, 0.35, 0.45));
  roof.position.y = 1.85;
  roof.rotation.y = Math.PI / 4;
  home.add(roof);
  scene.add(home);

  var keyGroup = new THREE.Group();
  keyGroup.position.set(1.8, 1.2, -1.2);
  var keyRing = new THREE.Mesh(new THREE.TorusGeometry(0.22, 0.04, 8, 24), mat(0xe8c96a, 0.55, 0.35));
  keyRing.rotation.x = Math.PI / 2;
  keyGroup.add(keyRing);
  var keyShaft = new THREE.Mesh(new THREE.BoxGeometry(0.08, 0.55, 0.08), mat(0xe8c96a, 0.5, 0.4));
  keyShaft.position.set(0.35, -0.15, 0);
  keyGroup.add(keyShaft);
  scene.add(keyGroup);

  /* Pilastro FISSO (stabile) */
  var fissoGroup = new THREE.Group();
  fissoGroup.position.set(-2.8, 0, -10);
  var fissoBase = new THREE.Mesh(new THREE.BoxGeometry(1.4, 0.15, 1.4), mat(0x1a2744, 0.1, 0.8));
  fissoBase.position.y = 0.08;
  fissoGroup.add(fissoBase);
  var fissoPillar = new THREE.Mesh(new THREE.BoxGeometry(0.9, 2.8, 0.9), mat(0x4a90d9, 0.25, 0.5));
  fissoPillar.position.y = 1.55;
  fissoPillar.castShadow = true;
  fissoGroup.add(fissoPillar);
  var fissoTop = new THREE.Mesh(new THREE.BoxGeometry(1.1, 0.2, 1.1), mat(0x7ec8ff, 0.3, 0.4));
  fissoTop.position.y = 3.05;
  fissoGroup.add(fissoTop);
  scene.add(fissoGroup);

  /* Pilastro VARIABILE (oscilla con scroll) */
  var varGroup = new THREE.Group();
  varGroup.position.set(2.8, 0, -10);
  var varBase = new THREE.Mesh(new THREE.BoxGeometry(1.4, 0.15, 1.4), mat(0x1a2744, 0.1, 0.8));
  varBase.position.y = 0.08;
  varGroup.add(varBase);
  var varPillar = new THREE.Mesh(new THREE.BoxGeometry(0.9, 2.2, 0.9), mat(0xff6b35, 0.25, 0.5));
  varPillar.position.y = 1.25;
  varPillar.castShadow = true;
  varGroup.add(varPillar);
  var varTop = new THREE.Mesh(new THREE.BoxGeometry(1.1, 0.2, 1.1), mat(0xff8f5e, 0.3, 0.4));
  varTop.position.y = 2.45;
  varGroup.add(varTop);
  scene.add(varGroup);

  /* Scudo under 36 / CONSAP */
  var shield = new THREE.Group();
  shield.position.set(0, 0, -20);
  var shieldBody = new THREE.Mesh(new THREE.CylinderGeometry(1.1, 1.1, 0.18, 6), mat(0xc9a84c, 0.4, 0.45));
  shieldBody.rotation.x = Math.PI / 2;
  shieldBody.position.y = 2.2;
  shield.add(shieldBody);
  var shieldRing = new THREE.Mesh(new THREE.TorusGeometry(1.15, 0.06, 8, 6), mat(0xe8c96a, 0.5, 0.35));
  shieldRing.rotation.x = Math.PI / 2;
  shieldRing.position.y = 2.2;
  shield.add(shieldRing);
  scene.add(shield);

  /* Curva Euribor (particelle) */
  var ptCount = reducedMotion ? 80 : 220;
  var pts = new Float32Array(ptCount * 3);
  for (var i = 0; i < ptCount * 3; i += 3) {
    pts[i] = (Math.random() - 0.5) * 10;
    pts[i + 1] = 1.5 + Math.random() * 2.5;
    pts[i + 2] = -8 - Math.random() * 28;
  }
  var ptGeo = new THREE.BufferGeometry();
  ptGeo.setAttribute('position', new THREE.BufferAttribute(pts, 3));
  var euriborPts = new THREE.Points(ptGeo, new THREE.PointsMaterial({
    size: 0.07, color: 0xff6b35, transparent: true, opacity: 0.6, sizeAttenuation: true
  }));
  scene.add(euriborPts);

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
    if (hintEl && targetProgress > 0.05) hintEl.classList.add('hidden');
  }

  function lerp(a, b, t) { return a + (b - a) * t; }
  function ease(t) { return t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2; }

  var animId;
  function animate() {
    animId = requestAnimationFrame(animate);
    smoothProgress = lerp(smoothProgress, targetProgress, reducedMotion ? 1 : 0.08);
    var p = ease(smoothProgress);

    camera.position.z = lerp(16, -36, p);
    camera.position.x = Math.sin(p * Math.PI * 1.5) * 0.9;
    camera.position.y = lerp(2.4, 3.2, Math.sin(p * Math.PI));
    camera.lookAt(0, 1.6, camera.position.z - 10);

    keyGroup.rotation.y = p * Math.PI * 2;
    home.rotation.y = Math.sin(p * Math.PI) * 0.12;

    var varH = 1.2 + Math.sin(p * Math.PI * 6) * 0.55;
    varPillar.scale.y = varH;
    varPillar.position.y = 0.15 + varH * 1.1;
    varTop.position.y = varPillar.position.y + varH * 1.1 + 0.2;

    fissoPillar.rotation.z = Math.sin(p * Math.PI * 2) * 0.02;
    shield.rotation.y = p * Math.PI * 0.5;

    if (!reducedMotion) {
      var arr = ptGeo.attributes.position.array;
      for (var j = 0; j < arr.length; j += 3) {
        arr[j + 1] += 0.008 + Math.sin(p * 4 + j) * 0.004;
        if (arr[j + 1] > 5) arr[j + 1] = 1.2;
      }
      ptGeo.attributes.position.needsUpdate = true;
    }

    blueLight.intensity = 0.4 + p * 0.35;
    orangeLight.intensity = 0.3 + Math.abs(Math.sin(p * Math.PI * 3)) * 0.4;

    renderer.render(scene, camera);
  }

  function onResize() {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
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
