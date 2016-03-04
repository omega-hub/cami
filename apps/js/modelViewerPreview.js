var scene = new THREE.Scene();
var camera = new THREE.PerspectiveCamera( 75, window.innerWidth / window.innerHeight, 0.1, 1000 );

var renderer = new THREE.WebGLRenderer();
// get the DOM element to attach to
// - assume we've got jQuery to hand
var $container = $('#header');
renderer.setSize( window.innerWidth, window.innerHeight );
renderer.setClearColor( 0x244040, 1 )
renderer.clear()
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

var material = new THREE.MeshPhongMaterial( {color: 0xEBBD68})
var cube = new THREE.Mesh( geometry, material );
cube.position.z = -5.2
ScrollSpeed = 0.1
addLights();
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
	camera.position.z = Math.max(Math.min(camera.position.z + (delta ),15),-10)
}

function setZoom3JS(z) {
    camera.position.z = z
}

function setPan3JS(x,y) {
    camera.position.x = x
    camera.position.y = y
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