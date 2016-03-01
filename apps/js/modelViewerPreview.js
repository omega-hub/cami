var scene = new THREE.Scene();
var camera = new THREE.PerspectiveCamera( 75, window.innerWidth / window.innerHeight, 0.1, 1000 );

var renderer = new THREE.WebGLRenderer();
// get the DOM element to attach to
// - assume we've got jQuery to hand
var $container = $('#header');
renderer.setSize( window.innerWidth, window.innerHeight );
// attach the render-supplied DOM element
$container.append(renderer.domElement);

var geometry = new THREE.BoxGeometry( 1, 1, 1 );
// The following code randomizes colors
// for ( var i = 0; i < geometry.faces.length; i ++ ) {
// 	var color = Math.random() * 0xffffff 
//     geometry.faces[ i ].color.setHex( color);
//     i ++
//     geometry.faces[ i ].color.setHex( color);
// }
// var material = new THREE.MeshPhongMaterial( { color: 0xffffff, vertexColors: THREE.FaceColors } );

var material = new THREE.MeshPhongMaterial( {color: 0xff0000})
var cube = new THREE.Mesh( geometry, material );
addLights();
scene.add( cube );

camera.position.z = 5;

function render() {
	requestAnimationFrame( render );
	renderer.render( scene, camera );
}
render();


function addLights() {
    var dirLight = new THREE.DirectionalLight(0xff0000, 1);
    dirLight.position.set(0, 0, 7);
    scene.add(dirLight);
}

function onZoom3JS(delta) {
	camera.position.z = camera.position.z - (delta * 0.1)
}


function onRotate3JS(dx,dy,dz) {
	var radX = dx * (Math.PI/180)
	var radY = dy * (Math.PI/180)
	var radZ = dz * (Math.PI/180)
    var xAxis = new THREE.Vector3(1,0,0);
    var yAxis = new THREE.Vector3(0,1,0);
    var zAxis = new THREE.Vector3(0,0,1);
    rotateAroundWorldAxis(cube,xAxis,radY)
    rotateAroundWorldAxis(cube,yAxis,radX)
    rotateAroundWorldAxis(cube,zAxis,radZ)
}

// Rotate an object around an arbitrary axis in object space
var rotObjectMatrix;
function rotateAroundObjectAxis(object, axis, radians) {
    rotObjectMatrix = new THREE.Matrix4();
    rotObjectMatrix.makeRotationAxis(axis.normalize(), radians);

    // old code for Three.JS pre r54:
    // object.matrix.multiplySelf(rotObjectMatrix);      // post-multiply
    // new code for Three.JS r55+:
    object.matrix.multiply(rotObjectMatrix);

    // old code for Three.js pre r49:
    // object.rotation.getRotationFromMatrix(object.matrix, object.scale);
    // old code for Three.js r50-r58:
    // object.rotation.setEulerFromRotationMatrix(object.matrix);
    // new code for Three.js r59+:
    object.rotation.setFromRotationMatrix(object.matrix);
}

var rotWorldMatrix;
// Rotate an object around an arbitrary axis in world space       
function rotateAroundWorldAxis(object, axis, radians) {
    rotWorldMatrix = new THREE.Matrix4();
    rotWorldMatrix.makeRotationAxis(axis.normalize(), radians);

    // old code for Three.JS pre r54:
    //  rotWorldMatrix.multiply(object.matrix);
    // new code for Three.JS r55+:
    rotWorldMatrix.multiply(object.matrix);                // pre-multiply

    object.matrix = rotWorldMatrix;

    // old code for Three.js pre r49:
    // object.rotation.getRotationFromMatrix(object.matrix, object.scale);
    // old code for Three.js pre r59:
    // object.rotation.setEulerFromRotationMatrix(object.matrix);
    // code for r59+:
    object.rotation.setFromRotationMatrix(object.matrix);
}

function onPan3JS(dx,dy,dz) {
    camera.position.x += dx
    camera.position.y += dy
    camera.position.z += dz
}