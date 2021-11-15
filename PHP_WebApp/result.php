<?php
	$server = "http://127.0.0.1:5000";
	$uploadDir = 'uploads/';
	
	function convertFileName($fileName){
		return md5(strval(microtime(true))."_CS406.M11".$fileName).".jpg";
	}
	
	function sendPostRequest($server, $image, $typeBlur, $kernelSize, $kernelDepth, $imageReplace){
		$data = array("image" => $image, "typeBlur" => $typeBlur, "kernelSize" => $kernelSize, "kernelDepth" => $kernelDepth, "imageReplace" => $imageReplace);
		$ch = curl_init($server);
		curl_setopt($ch, CURLOPT_POSTFIELDS, $data);
		curl_setopt($ch, CURLOPT_HTTPHEADER, array("Content-Type:multipart/form-data"));
		curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
		$result = curl_exec($ch);
		if (curl_getinfo($ch, CURLINFO_HTTP_CODE) != 200)
			header("Location: index.php?error=500");
		curl_close($ch);
		return $result;
	}
	
	$result = "";

	if (isset($_POST["submit"])) {
		$fileNameImage = convertFileName(basename($_FILES['image']['name']));
		$pathFileImage = $uploadDir.$fileNameImage;
		if (move_uploaded_file($_FILES['image']['tmp_name'], $pathFileImage)) {
			$image = curl_file_create($pathFileImage);
			$imageReplace = curl_file_create("images/_.jpg");
			$typeBlur = $_POST["typeBlur"];
			$kernelSize = $_POST["kernelSize"];
			$kernelDepth = $_POST["kernelDepth"];
			if ($typeBlur == "6") {
				$fileNameImageReplace = convertFileName(basename($_FILES['imageReplace']['name']));
				$pathFileImageReplace = $uploadDir.$fileNameImageReplace;
				if (move_uploaded_file($_FILES['imageReplace']['tmp_name'], $pathFileImageReplace)){
					$imageReplace = curl_file_create($pathFileImageReplace);
				}
			}
			$result = json_decode(sendPostRequest($server, $image, $typeBlur, $kernelSize, $kernelDepth, $imageReplace));
			
	
		} else {
			header("Location: index.php");
		}
	} else {
		header("Location: index.php");
	}
?>
<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate" />
  <meta http-equiv="Pragma" content="no-cache" />
  <meta http-equiv="Expires" content="0" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  
  <title>CS406.M11 - Nhận diện và làm mờ biển số</title>
  
  <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous">

  <style>
    .dashed-border {
      border: dashed 2px #dee2e6 !important;
    }

    input[type="range"]::-webkit-slider-thumb {
      background: #434343;
    }

    svg {
      fill: #dee2e6;
      transition: 0.75s;
    }

    svg:hover {
      fill: #6c757d;
    }

    select {
      -webkit-appearance: none;
      -moz-appearance: none;
      background: transparent;
      background-image: url("data:image/svg+xml;utf8,<svg fill='black' height='24' viewBox='0 0 24 24' width='24' xmlns='http://www.w3.org/2000/svg'><path d='M7 10l5 5 5-5z'/><path d='M0 0h24v24H0z' fill='none'/></svg>");
      background-repeat: no-repeat;

      background-position-x: 100%;
      background-position-y: 5px;
      padding: 1rem;
      padding-right: 2rem;
    }
	
	.footer {
		padding-top: 15px;
		padding-bottom: 5px;
		text-align: center;
		color: #000000;
		font-weight: bold;
	}
  </style>
</head>
<body>
  
  <div class="container mt-5">
    <div class="row">
      <div class="col">
        <div class="dashed-border w-100" style="height: 640px; display: flex; align-content: space-around; justify-content: center; flex-wrap: wrap;">
          <div class="text-center">
			<img style="max-height: 100%; max-width: 100%;" src="<?php echo $result->{'imageDes'}; ?>">
          </div>
        </div>
      </div>
    </div>
    <div class="row mt-3 mb-3">
      <div class="col text-center">
        <a type="submit" href="./index.php" class="btn btn-success">Go home</a>
        <a type="submit" href="<?php echo "./download.php?url=".$result->{'imageDes'}; ?>" target="_blank" class="btn btn-success">Download</a>
      </div>
    </div>
  </div>

	<div class="footer">
		&copy; 2021 - Team: 
		<a href="https://github.com/lphuong304">19520227</a> -
		<a href="https://github.com/nhalq">19520195</a> -
		<a href="https://github.com/caohungphu">19520214</a>
	</div>
</body>
</html>
