var scene = new THREE.Scene();
var camera = new THREE.PerspectiveCamera( 75, window.innerWidth / window.innerHeight, 0.1, 1000 );

var renderer = new THREE.WebGLRenderer();
// get the DOM element to attach to
// - assume we've got jQuery to hand
var $container = $('#header');
renderer.setSize( window.innerWidth, window.innerHeight );
renderer.setClearColor( 0Xf1f1f1, 1 )
renderer.clear()
// attach the render-supplied DOM element
$container.append(renderer.domElement);

var geometry = new THREE.BoxGeometry( 1, 1, 0.1);
var allScreen = new THREE.BoxGeometry(8,4.5,0.1);

var material = new THREE.MeshPhongMaterial( {color: 0xCCB233})
var cube = new THREE.Mesh( geometry, material );

var material = new THREE.MeshPhongMaterial( {color: 0x1E1ECC})
var backCube = new THREE.Mesh( allScreen, material );

backCube.position.z = -5.1
cube.position.z = -5
currentScale = 1.0
currentWidth = 1.0
currentHeight = 1.0
addLights();
scene.add( backCube );
scene.add( cube );

camera.position.z = 0;

THREEx.WindowResize(renderer, camera);

function render() {
    requestAnimationFrame( render );
    renderer.render( scene, camera );
}
render();

function addLights() {
    var dirLight = new THREE.DirectionalLight(0xffffff, 1);
    dirLight.position.set(0, 0, 3);
    scene.add(dirLight);
}

function onZoom3JS(delta) {
    cube.position.z = Math.max(Math.min(cube.position.z + (delta ),15),-10)
}
function setCurrentWidthHeight(width, height) {
    currentWidth = width
    currentHeight = height
    setZoom3JS(currentScale)
}
function setZoom3JS(z) {
    cube.scale.x = z * currentWidth
    cube.scale.y = z * currentHeight
    currentScale = z
}

function setPan3JS(x,y) {
    cube.position.x = x
    cube.position.y = y
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
    object.matrix.multiply(rotObjectMatrix);
    object.rotation.setFromRotationMatrix(object.matrix);
}

var rotWorldMatrix;
// Rotate an object around an arbitrary axis in world space       
function rotateAroundWorldAxis(object, axis, radians) {
    rotWorldMatrix = new THREE.Matrix4();
    rotWorldMatrix.makeRotationAxis(axis.normalize(), radians);
    rotWorldMatrix.multiply(object.matrix);                // pre-multiply

    object.matrix = rotWorldMatrix;
    object.rotation.setFromRotationMatrix(object.matrix);
}

function resetOrientation3JS() {
    cube.rotation.x = 0
    cube.rotation.y = 0
    cube.rotation.z = 0
}

function setCubeColor(hexColor) {
    cube.material.color.setHex(hexColor)
}

function setBackgroundColor(hexColor) {
    renderer.setClearColor( hexColor, 1 )
    renderer.clear()
}