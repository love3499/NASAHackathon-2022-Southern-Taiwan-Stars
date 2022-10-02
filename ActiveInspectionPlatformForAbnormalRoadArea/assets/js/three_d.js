import * as THREE from 'https://threejsfundamentals.org/threejs/resources/threejs/r132/build/three.module.js';
import {
    OrbitControls
} from 'https://threejsfundamentals.org/threejs/resources/threejs/r132/examples/jsm/controls/OrbitControls.js';
import {
    OBJLoader
} from 'https://threejsfundamentals.org/threejs/resources/threejs/r132/examples/jsm/loaders/OBJLoader.js';
import {
    MTLLoader
} from 'https://threejsfundamentals.org/threejs/resources/threejs/r132/examples/jsm/loaders/MTLLoader.js';

class td_loader {

    constructor() {
        var percent_offset = 0.0;
        var timer = setInterval(Add_Percent_To_Make_User_More_Patient, 100);

        function Add_Percent_To_Make_User_More_Patient() {
            percent_offset += 0.01;
        }

        function getOffset(el) {
            var _x = 0;
            var _y = 0;
            while (el && !isNaN(el.offsetLeft) && !isNaN(el.offsetTop)) {
                _x += el.offsetLeft - el.scrollLeft;
                _y += el.offsetTop - el.scrollTop;
                el = el.offsetParent;
            }
            return {
                top: _y,
                left: _x
            };
        }

        function three_d() {
            const canvas = document.querySelector('#c');
            const renderer = new THREE.WebGLRenderer({
                canvas
            });
            var texts = [];

            const fov = 45;
            const aspect = 2; // the canvas default
            const near = 0.1;
            const far = 10000;
            const camera = new THREE.PerspectiveCamera(fov, aspect, near, far);
            camera.position.set(0, 10, -40);
            camera.rotation.y = 0;

            const controls = new OrbitControls(camera, canvas);
            controls.target.set(0, 5, 0);
            controls.update();

            const scene = new THREE.Scene();

            $(canvas).on('mousemove', () => {
                texts.forEach(text => {
                    text.lookAt(camera.position);
                });
            });

            function add_text(text, x, y, z) {
                var textLoad = new THREE.FontLoader().load('assets/font/font.json', function (font) {
                    var txtGeo = new THREE.TextGeometry(text, {
                        font: font,
                        size: 2.0,
                        height: 0.1,
                        curveSegments: 12,
                        bevelEnabled: true,
                        bevelThickness: 0.1,
                        bevelSize: 0.05,
                        bevelSegments: 3
                    });
                    var txtMater = new THREE.MeshBasicMaterial({
                        color: 0xfc9003
                    });
                    var txtMesh = new THREE.Mesh(txtGeo, txtMater);
                    txtMesh.position.set(x, y, z);
                    texts.push(txtMesh);
                    scene.add(txtMesh);
                });
            }

            function add_img(url) {
                const texture = new THREE.TextureLoader().load(url);
                texture.wrapS = THREE.RepeatWrapping;
                texture.wrapT = THREE.RepeatWrapping;
                texture.repeat.set(1, 1);
                const geometry = new THREE.PlaneGeometry(16, 9);
                let pts = [
                    [0.5, 0.5],
                    [-0.5, 0.5],
                    [-0.5, -0.5],
                    [0.5, -0.5]
                ].map(p => {
                    return new THREE.Vector2(p[0], p[1])
                });
                let border_geometry = new THREE.BufferGeometry().setFromPoints(pts);
                border_geometry.setIndex([0, 1, 2, 3, 0]);
                border_geometry.scale(16, 9, 1);

                const planeMat = new THREE.MeshPhongMaterial({
                    map: texture,
                    side: THREE.DoubleSide,
                });
                const mesh = new THREE.Mesh(geometry, planeMat);
                mesh.rotation.y = Math.PI * -.5;
                scene.add(mesh);

                var outlineMaterial1 = new THREE.LineBasicMaterial({
                    color: 0xFF0000,
                    linewidth: 300,
                })

                var outlineMesh1 = new THREE.Line(border_geometry, outlineMaterial1);
                outlineMesh1.rotation.y = Math.PI * -.5;
                scene.add(outlineMesh1);
                return new Pic_Result(mesh, outlineMesh1);
            }

            function add_ball() {
                let geometry = new THREE.SphereGeometry(1, 32, 16);
                let material = new THREE.MeshBasicMaterial({
                    color: 0xff0000
                });
                let sphere = new THREE.Mesh(geometry, material);
                scene.add(sphere)
                return sphere;
            }

            scene.background = new THREE.Color('gray'); {
                add_img("assets/3d/pictures/1.jpg").Set_Position(78, 9, -9);
                add_text("Defect1", 78, 14, -9);
                add_ball().position.set(79, 5.5, 3);


                var img = add_img("assets/3d/pictures/2.jpg");
                img.Set_Position(65, 7, 3);
                img.Set_Rotation(0);
                add_text("Defect2", 65, 12, 3);
                add_ball().position.set(71, 11, 3);

                img = add_img("assets/3d/pictures/3.jpg");
                img.Set_Position(31, 6, 15);
                img.Set_Rotation(Math.PI * .5);
                add_text("Defect3", 31, 11, 15);
                add_ball().position.set(31, 11, 3);

                img = add_img("assets/3d/pictures/4.jpg");
                img.Set_Position(24.5, 5, -12);
                add_text("Defect4", 24.5, 10, -12);
                add_ball().position.set(24.5, 5, 2);

                img = add_img("assets/3d/pictures/5.jpg");
                img.Set_Position(12, 12, -7);
                img.Set_Rotation(0);
                add_text("Defect5", 12, 17, -7);
                add_ball().position.set(1, 12, -4);
            }

            const skyColor = 0xB1E1FF; // light blue
            const groundColor = 0xB97A20; // brownish orange
            const intensity = 1;
            scene.add(new THREE.HemisphereLight(skyColor, groundColor, intensity));

            const color = 0xFFFFFF;
            const light = new THREE.DirectionalLight(color, intensity);
            light.position.set(0, 10, 0);
            light.target.position.set(-5, 0, 0);
            scene.add(light);
            scene.add(light.target);

            const mtlLoader = new MTLLoader();
            mtlLoader.load(
                'assets/3d/model.mtl',
                (materials) => {
                    materials.preload();
                    const objLoader = new OBJLoader();
                    objLoader.setMaterials(materials);
                    console.log('loading model');
                    objLoader.load('assets/3d/model.obj', (root) => {
                        scene.add(root);
                        root.position.y += 30;
                        root.rotation.x = Math.PI * -.5;
                        render();
                        console.log('model loaded')
                        $("#loading").hide();
                        clearInterval(timer);
                    },
                        function (xhr) {
                            let offsetted_percent = Math.round(((xhr.loaded / xhr.total) * 85 + percent_offset) * 10) / 10;
                            if (offsetted_percent > 100)
                                offsetted_percent = 100;
                            $("#loading").html('Loading...' + offsetted_percent + '%');
                        },);
                    // $("#loading").hide();

                },
                (xhr) => {
                    console.log((xhr.loaded / xhr.total) * 100 + '% loaded')
                },
                (error) => {
                    console.log('An error happened')
                }
            )

            function resizeRendererToDisplaySize(renderer) {
                const canvas = renderer.domElement;
                const width = canvas.clientWidth;
                const height = canvas.clientHeight;
                const needResize = canvas.width !== width || canvas.height !== height;
                if (needResize) {
                    renderer.setSize(width, height, false);
                }
                return needResize;
            }

            function render() {

                if (resizeRendererToDisplaySize(renderer)) {
                    const canvas = renderer.domElement;
                    camera.aspect = canvas.clientWidth / canvas.clientHeight;
                    camera.updateProjectionMatrix();
                }

                renderer.render(scene, camera);

                requestAnimationFrame(render);
            }
            requestAnimationFrame(render);
        }
        hide_3d();
        three_d();
    }
}