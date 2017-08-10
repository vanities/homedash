<?php 
// save-image.php
// From Zipso.net - http://zipso.net/a-simple-touchscreen-sketchpad-using-javascript-and-html5/
// Adapted From - http://stackoverflow.com/a/13199011/1788488
//
// Retrieves image data sent within a form, and sends it back to the browser with headers
// that indicate that it should be downloaded. This script does not save the file itself on the 
// server, but it could be adapted to, since the binary image data is available right after the base64_decode.

$filename = date(jMy) . ".png"; // The filename - this could be specified by the user as another form field
$filetype = "png"; // The file image type

// Read the uploaded file from the form data and convert it to binary format
$img = $_POST['save_remote_data'];
$img = str_replace('data:image/png;base64,', '', $img);
$img = str_replace(' ', '+', $img);
$data = base64_decode($img);

// Output "Download"-type headers to browser
header("Content-Type: image/".$filetype);
header("Content-Length: " .(string)(filesize($file)) );
header("Content-Disposition: attachment; filename=\"$filename\"");
header("Content-Transfer-Encoding: binary\n");

// Output the binary image data itself
echo($data);
?>
