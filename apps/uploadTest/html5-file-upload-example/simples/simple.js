/**
 * Created by remi on 17/01/15.
 */
(function () {

    /**
     * A simple function to display file informations
     */
    function showFileInfo(file){
        console.log("name : " + file.name);
        console.log("size : " + file.size);
        console.log("type : " + file.type);
        console.log("date : " + file.lastModified);
    }


    var fileInput1 = document.querySelector('#simplefile');
    fileInput1.addEventListener('change', function () {
        var fileSelected = this.files[0];
        showFileInfo(fileSelected);
    }, false);


    var fileInput2 = document.querySelector('#multiplefiles');
    fileInput2.addEventListener('change', function () {
        var files = this.files;

        for(var i=0; i<files.length; i++){
            console.group('File '+i);
            showFileInfo(files[i]);
            console.groupEnd();
        }
    }, false);


    var fileInput3 = document.querySelector('#multiplefilesfilter');
    fileInput3.addEventListener('change', function () {
        var files = this.files;
        for(var i=0; i<files.length; i++){
            console.group('File '+i);
            showFileInfo(files[i]);
            console.groupEnd();
        }
    }, false);

}());