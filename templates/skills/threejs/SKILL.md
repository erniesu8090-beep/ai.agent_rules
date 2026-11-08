---
name: threejs
description: Three.js r170 現代 Web 3D 開發與互動檢視器指引。涵蓋最新繁中文件、ES Module / Import Map 單檔架構、模型載入（GLTF/GLB）、場景/相機/光源配置與即時渲染最佳實踐。當使用者提到「Three.js」、「Web 3D」、「WebGL 渲染」、「網頁 3D 檢視器」、「3D 數據視覺化」時載入。
---

# Three.js r170 現代 Web 3D 開發與檢視器指引

本技能提供在任何專案中開發網頁 3D 視覺化、單檔 HTML 3D 工具以及 3D 模型檢視器（GLTF/GLB）的標準架構、現代 API 規範與防坑守則。

---

## 1. 核心文件與權威參考

- **Three.js r170 繁中說明文件（HighQ77 整理）**：  
  👉 <https://highq77.github.io/threejs-r170-doc/>  
  - 整理自官方 r170（0.170.0）架構，涵蓋 24 篇教學指南與 287 個 API 條目。
  - **內建即時執行編輯器**：支援在沙箱 iframe 中直接 `Ctrl + Enter` 測試程式碼，修改即時渲染，免裝本地環境即可驗證效果。
- **官方英文文件**：<https://threejs.org/docs/>
- **官方 GitHub 原始碼（r170）**：<https://github.com/mrdoob/three.js/tree/r170>

---

## 2. 適用情境

1. **免安裝單檔 HTML 3D 工具**：提供給同事、客戶免設定環境，以瀏覽器直接點開運作的 3D 檢視或動態圖表。
2. **本地 3D 模型預覽**：搭配既有 `07-web3d-extract` 技能從網頁提取之 `.glb` / `.gltf` 模型，快速在本地建置含軌道控制、打光與材質檢視的預覽介面。
3. **網頁 3D 數據視覺化與特效**：空間粒子、幾何變形、自訂著色器（ShaderMaterial）與後期特效（Post-processing）。

---

## 3. r170 現代規範與防坑守則（避開舊版廢棄語法）

在撰寫 Three.js 程式碼時，**嚴禁套用舊版教程過時寫法**，必須遵守以下 r170 規範：

1. **模組導入**：全面採用 ES Modules 與 `<script type="importmap">`，禁止在 HTML 引入全域 `three.min.js`。附加模組一律自 `three/addons/`（或 `three/examples/jsm/`）導入。
2. **色彩空間（Color Space）**：
   - 渲染器設定：使用 `renderer.outputColorSpace = THREE.SRGBColorSpace;`（**嚴禁使用已棄用的 `renderer.outputEncoding`**）。
   - 顏色/漫反射貼圖：`texture.colorSpace = THREE.SRGBColorSpace;`；法線、金屬度、粗糙度貼圖則保持線性空間預設（`THREE.NoColorSpace`）。
3. **幾何體全面使用 BufferGeometry**：
   - **嚴禁使用 `THREE.Geometry`**（已被官方徹底移除）。所有內建幾何體均為 `BoxGeometry`、`SphereGeometry` 等 BufferGeometry 子類。
4. **真實物理光照**：
   - 光源衰減與強度符合物理特性，環境光（`AmbientLight`）強度建議 `0.5 ~ 1.0`，主方向光（`DirectionalLight`）建議 `1.0 ~ 2.5`。
5. **DPI 與效能自保**：
   - 渲染器像素比必須設為 `renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));`，防止在高解析度螢幕（4K/Retina）狂飆像素導致 GPU 卡死。

---

## 4. 單檔自包含 HTML 快速起手式模板

可直接存為單一 `.html` 檔案雙擊開啟（需透過本地伺服器或允許跨域 CDN 連線）：

```html
<!DOCTYPE html>
<html lang="zh-TW">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Three.js r170 現代 Web 3D 模板</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body { overflow: hidden; background: #1a1a1a; font-family: sans-serif; }
    #canvas-container { width: 100vw; height: 100vh; display: block; }
    #ui-overlay { position: absolute; top: 16px; left: 16px; color: #fff; pointer-events: none; }
  </style>
  <script type="importmap">
    {
      "imports": {
        "three": "https://unpkg.com/three@0.170.0/build/three.module.js",
        "three/addons/": "https://unpkg.com/three@0.170.0/examples/jsm/"
      }
    }
  </script>
</head>
<body>
  <div id="ui-overlay">
    <h2>Three.js r170 互動檢視</h2>
    <p>左鍵旋轉 / 右鍵平移 / 滾輪縮放</p>
  </div>
  <div id="canvas-container"></div>

  <script type="module">
    import * as THREE from 'three';
    import { OrbitControls } from 'three/addons/controls/OrbitControls.js';

    // 1. 場景
    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0x1a1a1a);

    // 2. 相機
    const camera = new THREE.PerspectiveCamera(60, window.innerWidth / window.innerHeight, 0.1, 1000);
    camera.position.set(3, 3, 5);

    // 3. 渲染器
    const container = document.getElementById('canvas-container');
    const renderer = new THREE.WebGLRenderer({ antialias: true, powerPreference: 'high-performance' });
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.outputColorSpace = THREE.SRGBColorSpace;
    renderer.shadowMap.enabled = true;
    renderer.shadowMap.type = THREE.PCFSoftShadowMap;
    container.appendChild(renderer.domElement);

    // 4. 控制器
    const controls = new OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.dampingFactor = 0.05;

    // 5. 光源配置（三點光）
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.7);
    scene.add(ambientLight);

    const dirLight = new THREE.DirectionalLight(0xffffff, 1.5);
    dirLight.position.set(5, 10, 7);
    dirLight.castShadow = true;
    dirLight.shadow.mapSize.width = 2048;
    dirLight.shadow.mapSize.height = 2048;
    scene.add(dirLight);

    // 6. 範例物件與陰影地板
    const floorGeo = new THREE.PlaneGeometry(20, 20);
    const floorMat = new THREE.MeshStandardMaterial({ color: 0x2a2a2a, roughness: 0.8 });
    const floor = new THREE.Mesh(floorGeo, floorMat);
    floor.rotation.x = -Math.PI / 2;
    floor.receiveShadow = true;
    scene.add(floor);

    const cubeGeo = new THREE.BoxGeometry(1.5, 1.5, 1.5);
    const cubeMat = new THREE.MeshStandardMaterial({ color: 0x38bdf8, roughness: 0.3, metalness: 0.2 });
    const cube = new THREE.Mesh(cubeGeo, cubeMat);
    cube.position.y = 1;
    cube.castShadow = true;
    scene.add(cube);

    // 7. RWD 視窗自動適應
    window.addEventListener('resize', () => {
      camera.aspect = window.innerWidth / window.innerHeight;
      camera.updateProjectionMatrix();
      renderer.setSize(window.innerWidth, window.innerHeight);
      renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    });

    // 8. 渲染迴圈
    function animate() {
      requestAnimationFrame(animate);
      cube.rotation.y += 0.005;
      controls.update();
      renderer.render(scene, camera);
    }
    animate();
  </script>
</body>
</html>
```

---

## 5. 本地 3D 模型載入器（GLTFLoader 整合模板）

搭配 `07-web3d-extract` 提取的 `.glb` 模型，載入時必須自動**置中**並**校正相機視距**：

```javascript
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';

const loader = new GLTFLoader();
loader.load('model.glb', (gltf) => {
  const model = gltf.scene;

  // 啟用所有網格的陰影
  model.traverse((node) => {
    if (node.isMesh) {
      node.castShadow = true;
      node.receiveShadow = true;
      if (node.material && node.material.map) {
        node.material.map.colorSpace = THREE.SRGBColorSpace;
      }
    }
  });

  // 自動計算邊界框並置中
  const box = new THREE.Box3().setFromObject(model);
  const size = box.getSize(new THREE.Vector3());
  const center = box.getCenter(new THREE.Vector3());

  model.position.x -= center.x;
  model.position.y -= box.min.y; // 讓模型底部貼齊 y=0 地面
  model.position.z -= center.z;

  scene.add(model);

  // 依模型最大尺寸自動調整相機距離
  const maxDim = Math.max(size.x, size.y, size.z);
  camera.position.set(maxDim * 1.5, maxDim * 1.2, maxDim * 2.0);
  controls.target.set(0, size.y / 2, 0);
  controls.update();
}, undefined, (error) => {
  console.error('載入 GLTF 失敗：', error);
});
```

---

## 6. 記憶體釋放與防洩漏（Resource Disposal）

在動態切換 3D 模型或銷毀檢視器元件時，必須主動遞迴釋放 WebGL 資源：

```javascript
function disposeHierarchy(node) {
  if (!node) return;
  if (node.geometry) node.geometry.dispose();
  if (node.material) {
    if (Array.isArray(node.material)) {
      node.material.forEach(m => disposeMaterial(m));
    } else {
      disposeMaterial(node.material);
    }
  }
  if (node.children) {
    node.children.forEach(child => disposeHierarchy(child));
  }
}

function disposeMaterial(mat) {
  for (const key of Object.keys(mat)) {
    const value = mat[key];
    if (value && typeof value.dispose === 'function') {
      value.dispose();
    }
  }
  mat.dispose();
}
```

---

## 7. 管制機與離線環境支援

在無法連線 `unpkg.com` 的封閉網路（如管制機或無外網內網）中：
1. 將 `three.module.js`、`OrbitControls.js`、`GLTFLoader.js` 等靜態檔案下載至專案的 `assets/vendor/three/` 目錄。
2. 將 `<script type="importmap">` 改為本機相對路徑：
   ```json
   {
     "imports": {
       "three": "./assets/vendor/three/three.module.js",
       "three/addons/": "./assets/vendor/three/addons/"
     }
   }
   ```
