<?php
/**
 * Created by IntelliJ IDEA.
 * User: remi
 * Date: 17/01/15
 * Time: 11:41
 */
if (isset($_FILES['uploaded_file'])) {
    // Example:
    if(move_uploaded_file($_FILES['uploaded_file']['tmp_name'], "datas/" . $_FILES['uploaded_file']['name'])){
        echo $_FILES['uploaded_file']['name']. " uploaded ...";
    } else {
        echo $_FILES['uploaded_file']['name']. " NOT uploaded ...";
    }

    exit;
} else {
    echo "no";
}