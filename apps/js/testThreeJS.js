var scene = new THREE.Scene();
var camera = new THREE.PerspectiveCamera( 75, window.innerWidth / window.innerHeight, 0.1, 1000 );

var renderer = new THREE.WebGLRenderer();
renderer.setSize( window.innerWidth, window.innerHeight );
document.body.appendChild( renderer.domElement );

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
	cube.rotation.x += 0.1;
	cube.rotation.y += 0.1;
	requestAnimationFrame( render );
	renderer.render( scene, camera );
}
render();


function addLights() {
    var dirLight = new THREE.DirectionalLight(0xff0000, 1);
    dirLight.position.set(0, 0, 7);
    scene.add(dirLight);
}