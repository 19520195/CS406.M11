<?php
    $fileUrl = $_GET['url'];
	header('Content-Disposition: attachment; filename="cs406.m11_result.jpg"');
	header("Content-Type: image/jpg");
	echo file_get_contents($fileUrl);
?>