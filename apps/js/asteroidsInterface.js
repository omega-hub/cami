var scene = new THREE.Scene();
var camera = new THREE.PerspectiveCamera( 75, window.innerWidth / window.innerHeight, 0.1, 1000 );

var renderer = new THREE.WebGLRenderer();
var fireDown = false
var thrustDown = false
// get the DOM element to attach to
// - assume we've got jQuery to hand
var $container = $('#header');
renderer.setSize( window.innerWidth, window.innerHeight );
renderer.setClearColor( 0Xf1f1f1, 1 )
renderer.clear()
// attach the render-supplied DOM element
$container.append(renderer.domElement);

var geometry = new THREE.BoxGeometry( 1, 1, 1 );

var material = new THREE.MeshPhongMaterial( {color: 0X3b5a5f})
var mat2 = new THREE.MeshPhongMaterial( {color: 0X3b5a5f})
var mat2 = new THREE.MeshPhongMaterial( {color: 0X3b5a5f})
console.log("making sprite buttons")
var map = new THREE.TextureLoader().load( "js/fire_button.png" );
var materialSpr = new THREE.SpriteMaterial( { map: map, color: 0xffffff, fog: true } );
var sprite = new THREE.Sprite( materialSpr );
scene.add( sprite );
sprite.position.z = -5
sprite.position.x = -2.5
sprite.position.y = -2.6

var spriteRight = new THREE.Sprite( materialSpr );
scene.add( spriteRight );
spriteRight.position.z = -5
spriteRight.position.x = 2.5
spriteRight.position.y = -2.6

var mapdown = new THREE.TextureLoader().load( "js/fire_buttondown.png" );
var materialSprdown = new THREE.SpriteMaterial( { map: mapdown, color: 0xffffff, fog: true } );
var spritedown = new THREE.Sprite( materialSprdown );
scene.add( spritedown );
spritedown.position.z = -5
spritedown.position.x = -2.5
spritedown.position.y = -2.6

var spritedownRight = new THREE.Sprite( materialSprdown );
scene.add( spritedownRight );
spritedownRight.position.z = -5
spritedownRight.position.x = -2.5
spritedownRight.position.y = -2.6

var map2 = new THREE.TextureLoader().load( "js/thrust_button.png" );
var materialSpr2 = new THREE.SpriteMaterial( { map: map2, color: 0xffffff, fog: true } );
var sprite2 = new THREE.Sprite( materialSpr2 );
scene.add( sprite2 );
sprite2.position.z = -5
sprite2.position.x = -1.5
sprite2.position.y = -2.6

var sprite2Right = new THREE.Sprite( materialSpr2 );
scene.add( sprite2Right );
sprite2Right.position.z = -5
sprite2Right.position.x = 1.5
sprite2Right.position.y = -2.6

var map2down = new THREE.TextureLoader().load( "js/thrust_buttondown.png" );
var materialSpr2down  = new THREE.SpriteMaterial( { map: map2down , color: 0xffffff, fog: true } );
var sprite2down  = new THREE.Sprite( materialSpr2down  );
scene.add( sprite2down );
sprite2down.position.z = -5
sprite2down.position.x = -1.5
sprite2down.position.y = -2.6

var sprite2downRight = new THREE.Sprite( materialSpr2down );
scene.add( sprite2downRight );
sprite2downRight.position.z = -5
sprite2downRight.position.x = 1.5
sprite2downRight.position.y = -2.6

var rocketMap = new THREE.TextureLoader().load( "js/rocket.png" );
var rocketMat = new THREE.SpriteMaterial( { map: rocketMap, color: 0xffffff, fog: true } );
var rocket = new THREE.Sprite( rocketMat );
scene.add( rocket );
rocket.position.z = -5

// var cube = new THREE.Mesh( geometry, material );
// cube.position.z = -5
// ScrollSpeed = 0.1
// addLights();
// scene.add( cube );

camera.position.z = 0;

THREEx.WindowResize(renderer, camera);

function render() {
	requestAnimationFrame( render );
	renderer.render( scene, camera );
    if (fireDown == true){
        spritedown.position.x = -2.5
        sprite.position.x = -12
        spritedownRight.position.x = 2.5
        spriteRight.position.x=15
    }
    else{
        spritedown.position.x = -15
        sprite.position.x = -2.5
        spritedownRight.position.x = 15
        spriteRight.position.x=2.5
    }

    if (thrustDown == true){
        sprite2down.position.x = -1.5
        sprite2.position.x = -15
        sprite2downRight.position.x = 1.5
        sprite2Right.position.x=15
    }
    else{
        sprite2down.position.x = -15
        sprite2.position.x = -1.5
        sprite2downRight.position.x = 15
        sprite2Right.position.x=1.5
    }
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

function setRocketAngle(angle) {
    rocketMat.rotation = angle
}

function setRocketPos(x,y) {
    rocket.position.x = (x - 384)/140
    rocket.position.y = (y + 512)/140
}

function setBackgroundColor(hexColor) {
    renderer.setClearColor( hexColor, 1 )
    renderer.clear()
}