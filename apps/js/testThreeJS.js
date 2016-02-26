var scene = new THREE.Scene();
var camera = new THREE.PerspectiveCamera( 75, window.innerWidth / window.innerHeight, 0.1, 1000 );

var renderer = new THREE.WebGLRenderer();
// get the DOM element to attach to
// - assume we've got jQuery to hand
var $container = $('#test');
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

function onMouseWheel3JS(delta) {
	camera.position.z = camera.position.z - (delta * 0.1)
}

function onRotate3JS(dx,dy,dz) {
	var radX = dx * (Math.PI/180)
	var radY = dy * (Math.PI/180)
	var radZ = dz * (Math.PI/180)
    cube.rotation.y += radX
    cube.rotation.x += radY
    cube.rotation.z += radZ
}