/**
 * Scroll 3D — mercato Limena (zona Imma)
 * Three.js locale · niente CDN · camera guidata dallo scroll
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
  scene.background = new THREE.Color(0x0d1a2a);
  scene.fog = new THREE.Fog(0x0d1a2a, 12, 55);

  var camera = new THREE.PerspectiveCamera(68, window.innerWidth / window.innerHeight, 0.1, 120);
  camera.position.set(0, 2.2, 18);

  var renderer = new THREE.WebGLRenderer({ antialias: true, alpha: false, powerPreference: 'high-performance' });
  renderer.setSize(window.innerWidth, window.innerHeight);
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, reducedMotion ? 1 : 1.75));
  renderer.shadowMap.enabled = !reducedMotion;
  if (renderer.shadowMap.enabled) renderer.shadowMap.type = THREE.PCFSoftShadowMap;
  wrap.appendChild(renderer.domElement);

  var ambient = new THREE.AmbientLight(0xffffff, 0.35);
  scene.add(ambient);

  var sun = new THREE.DirectionalLight(0xffeedd, 0.85);
  sun.position.set(6, 14, 10);
  if (renderer.shadowMap.enabled) {
    sun.castShadow = true;
    sun.shadow.mapSize.set(1024, 1024);
  }
  scene.add(sun);

  var goldLight = new THREE.PointLight(0xc9a84c, 0.55, 28);
  goldLight.position.set(-3, 5, -8);
  scene.add(goldLight);

  var accentLight = new THREE.PointLight(0xff6b35, 0.35, 22);
  accentLight.position.set(4, 4, -22);
  scene.add(accentLight);

  function makeMat(color, metal, rough) {
    return new THREE.MeshStandardMaterial({
      color: color,
      metalness: metal || 0.15,
      roughness: rough || 0.65
    });
  }

  var floorGeo = new THREE.PlaneGeometry(14, 70);
  var floor = new THREE.Mesh(floorGeo, makeMat(0x1a2744, 0.1, 0.85));
  floor.rotation.x = -Math.PI / 2;
  floor.position.set(0, 0, -18);
  floor.receiveShadow = true;
  scene.add(floor);

  var road = new THREE.Mesh(new THREE.PlaneGeometry(3.2, 70), makeMat(0x243552, 0.05, 0.9));
  road.rotation.x = -Math.PI / 2;
  road.position.set(0, 0.01, -18);
  scene.add(road);

  var houses = [];
  var housePositions = [
    { x: -4.2, z: -2, sold: false, scale: 1 },
    { x: 4.5, z: -8, sold: true, scale: 0.95 },
    { x: -3.8, z: -16, sold: true, scale: 1.05 },
    { x: 4.0, z: -24, sold: false, scale: 1 },
    { x: -4.5, z: -32, sold: true, scale: 0.9 }
  ];

  function buildHouse(opts) {
    var g = new THREE.Group();
    var s = opts.scale || 1;
    var body = new THREE.Mesh(new THREE.BoxGeometry(2.4 * s, 1.8 * s, 2 * s), makeMat(opts.sold ? 0x3a4a62 : 0x2C4A6E, 0.2, 0.7));
    body.position.y = 0.9 * s;
    body.castShadow = true;
    body.receiveShadow = true;
    g.add(body);

    var roof = new THREE.Mesh(new THREE.ConeGeometry(1.85 * s, 1.1 * s, 4), makeMat(opts.sold ? 0x4a5568 : 0xc9a84c, 0.35, 0.5));
    roof.position.y = 2.35 * s;
    roof.rotation.y = Math.PI / 4;
    roof.castShadow = true;
    g.add(roof);

    var door = new THREE.Mesh(new THREE.BoxGeometry(0.45 * s, 0.75 * s, 0.08), makeMat(0x152435, 0.1, 0.8));
    door.position.set(0, 0.38 * s, 1.02 * s);
    g.add(door);

    var winMat = makeMat(0x7ec8ff, 0.6, 0.2);
    [[-0.65, 1.1], [0.65, 1.1]].forEach(function (w) {
      var win = new THREE.Mesh(new THREE.BoxGeometry(0.42 * s, 0.42 * s, 0.06), winMat);
      win.position.set(w[0] * s, w[1] * s, 1.02 * s);
      g.add(win);
    });

    if (opts.sold) {
      var sign = new THREE.Mesh(new THREE.BoxGeometry(1.1 * s, 0.35 * s, 0.05), makeMat(0x8b2635, 0.1, 0.6));
      sign.position.set(0, 2.9 * s, 0.6 * s);
      g.add(sign);
    }

    g.position.set(opts.x, 0, opts.z);
    g.userData.sold = opts.sold;
    return g;
  }

  housePositions.forEach(function (hp) {
    var h = buildHouse(hp);
    scene.add(h);
    houses.push(h);
  });

  /* Bilancia domanda/offerta */
  var scaleGroup = new THREE.Group();
  scaleGroup.position.set(0, 0, -12);
  var pole = new THREE.Mesh(new THREE.CylinderGeometry(0.08, 0.08, 3.2, 12), makeMat(0xc9a84c, 0.5, 0.4));
  pole.position.y = 1.6;
  scaleGroup.add(pole);

  var beam = new THREE.Mesh(new THREE.BoxGeometry(4.2, 0.12, 0.12), makeMat(0xe8c96a, 0.4, 0.45));
  beam.position.y = 3.1;
  scaleGroup.add(beam);

  var panL = new THREE.Mesh(new THREE.CylinderGeometry(0.9, 0.75, 0.08, 24), makeMat(0x2C4A6E, 0.3, 0.5));
  panL.position.set(-1.8, 2.5, 0);
  scaleGroup.add(panL);

  var panR = new THREE.Mesh(new THREE.CylinderGeometry(0.9, 0.75, 0.08, 24), makeMat(0xFF6B35, 0.25, 0.5));
  panR.position.set(1.8, 2.2, 0);
  scaleGroup.add(panR);

  var offerBlock = new THREE.Mesh(new THREE.BoxGeometry(0.5, 0.5, 0.5), makeMat(0x2C4A6E, 0.2, 0.6));
  offerBlock.position.set(-1.8, 2.95, 0);
  scaleGroup.add(offerBlock);

  for (var bi = 0; bi < 5; bi++) {
    var buyer = new THREE.Mesh(new THREE.SphereGeometry(0.22, 12, 12), makeMat(0xff6b35, 0.4, 0.35));
    buyer.position.set(1.8 + (bi % 3) * 0.35 - 0.35, 2.65 + Math.floor(bi / 3) * 0.35, (bi % 2) * 0.25);
    scaleGroup.add(buyer);
  }
  scene.add(scaleGroup);

  /* Particelle = domanda acquirenti */
  var particleCount = reducedMotion ? 120 : 380;
  var positions = new Float32Array(particleCount * 3);
  for (var i = 0; i < particleCount * 3; i += 3) {
    positions[i] = (Math.random() - 0.5) * 12;
    positions[i + 1] = Math.random() * 6 + 0.5;
    positions[i + 2] = Math.random() * -48 - 2;
  }
  var particles = new THREE.BufferGeometry();
  particles.setAttribute('position', new THREE.BufferAttribute(positions, 3));
  var particleMat = new THREE.PointsMaterial({
    size: 0.06,
    color: 0xff6b35,
    transparent: true,
    opacity: 0.55,
    sizeAttenuation: true
  });
  var particleSystem = new THREE.Points(particles, particleMat);
  scene.add(particleSystem);

  /* Cartello prezzo unico disponibile */
  var priceSign = new THREE.Group();
  priceSign.position.set(0, 0, -28);
  var post = new THREE.Mesh(new THREE.CylinderGeometry(0.06, 0.06, 2.4, 8), makeMat(0xc9a84c, 0.4, 0.5));
  post.position.y = 1.2;
  priceSign.add(post);
  var board = new THREE.Mesh(new THREE.BoxGeometry(2.2, 0.9, 0.08), makeMat(0xc9a84c, 0.3, 0.45));
  board.position.y = 2.5;
  priceSign.add(board);
  scene.add(priceSign);

  var scrollMax = 1;
  var targetProgress = 0;
  var smoothProgress = 0;

  function calcScrollMax() {
    if (!scrollLayer) return 1;
    return Math.max(window.innerHeight * 4, scrollLayer.offsetHeight - window.innerHeight);
  }

  function onScroll() {
    var max = calcScrollMax();
    scrollMax = max;
    targetProgress = Math.min(1, Math.max(0, window.scrollY / max));
    if (progressEl) progressEl.style.width = (targetProgress * 100) + '%';
    if (hintEl && targetProgress > 0.06) hintEl.classList.add('hidden');
  }

  function lerp(a, b, t) {
    return a + (b - a) * t;
  }

  function easeInOutCubic(t) {
    return t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
  }

  var animId;
  function animate() {
    animId = requestAnimationFrame(animate);
    smoothProgress = lerp(smoothProgress, targetProgress, reducedMotion ? 1 : 0.08);
    var p = easeInOutCubic(smoothProgress);

    camera.position.z = lerp(18, -38, p);
    camera.position.x = Math.sin(p * Math.PI * 2) * 1.2;
    camera.position.y = lerp(2.2, 3.4, Math.sin(p * Math.PI));
    camera.lookAt(0, 1.8, camera.position.z - 12);

    scaleGroup.rotation.z = lerp(0.35, -0.35, p);
    beam.rotation.z = lerp(0.35, -0.35, p);
    panL.position.y = lerp(2.5, 3.1, p);
    panR.position.y = lerp(3.1, 2.2, p);

    houses.forEach(function (h, idx) {
      h.rotation.y = Math.sin(p * Math.PI + idx) * 0.08;
    });

    priceSign.rotation.y = Math.sin(p * Math.PI * 4) * 0.12;

    if (!reducedMotion) {
      var posArr = particles.attributes.position.array;
      for (var j = 1; j < posArr.length; j += 3) {
        posArr[j] -= 0.012 + p * 0.02;
        if (posArr[j] < 0.3) posArr[j] = 6.5;
      }
      particles.attributes.position.needsUpdate = true;
    }

    goldLight.intensity = 0.45 + p * 0.35;
    accentLight.intensity = 0.25 + p * 0.45;

    renderer.render(scene, camera);
  }

  function onResize() {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
    calcScrollMax();
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
    scene.traverse(function (obj) {
      if (obj.geometry) obj.geometry.dispose();
      if (obj.material) {
        if (Array.isArray(obj.material)) obj.material.forEach(function (m) { m.dispose(); });
        else obj.material.dispose();
      }
    });
  });
})();
