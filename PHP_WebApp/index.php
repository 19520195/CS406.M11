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
  <script src="//cdn.jsdelivr.net/npm/sweetalert2@11"></script>
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
<?php
	if (isset($_GET['error'])){
		if ($_GET['error'] == 500){
			echo "<script>Swal.fire('ERROR!','Server is down!','error');</script>";
		}
		
	}
?>
  <form class="container mt-5" method="POST" action="result.php" enctype="multipart/form-data">
    <div class="row">
      <div class="col-8">
        <div id="selector" class="dashed-border w-100" style="height: 512px; display: flex; align-content: space-around; justify-content: center; flex-wrap: wrap;">
          <div class="text-center">
            <img id="image" style="max-height: 100%; max-width: 100%; display: none;">
            <svg id="cat" width="136" height="98" viewBox="0 0 136 98"  xmlns="http://www.w3.org/2000/svg"><path data-v-f60c0bf8="" d="M134.297 23.2994C130.526 22.7207 131.321 31.6211 123.246 40.5079C119.998 44.0804 111.91 47.9403 108.242 49.5742C102.565 42.6453 91.956 38.55 76.7424 37.1206C61.713 35.7105 48.5971 34.2271 46.1097 29.503C42.8487 23.2974 46.2221 4.3605 45.2586 3.68921C43.8413 2.70157 40.4329 4.78295 38.3623 6.1564C35.8419 4.70386 32.3521 3.85125 27.5362 3.97085C23.4919 4.07116 20.5566 3.71815 16.9039 4.81767C16.7876 2.33313 17.0222 -0.25558 15.7697 0.0202667C9.38921 1.43229 4.42593 10.46 2.0044 19.1964C-1.95846 36.5574 0.736461 56.3064 3.38483 66.0555L3.28789 66.0401C3.28789 66.0401 12.4292 96.2617 14.3389 97.3554C15.4751 98.0035 15.5448 96.1536 15.5448 96.1536C15.6138 96.5207 15.818 96.849 16.1174 97.0741C16.4169 97.2992 16.79 97.4051 17.1637 97.3708C18.4821 97.2956 18.2998 95.8797 18.2998 95.8797C18.2998 95.8797 18.4627 97.1895 19.5562 97.0371C21.1072 96.8307 20.26 90.629 20.5779 87.4732C20.8164 85.0966 21.5589 83.1947 24.407 82.5369C25.5179 82.6931 27.1814 82.4751 28.366 82.6198C31.4215 83.5129 32.5034 85.4516 32.9163 88.0789C33.4088 91.2116 32.9163 97.4519 34.4673 97.5714C35.5686 97.6563 35.6558 96.3388 35.6558 96.3388C35.6558 96.3388 35.553 97.7624 36.8753 97.7643C37.2508 97.779 37.6182 97.6533 37.9053 97.4119C38.1923 97.1706 38.3782 96.8312 38.4263 96.4603C38.4263 96.4603 38.5989 98.3045 39.6962 97.5946C40.5318 97.0545 42.4609 90.8122 44.3279 84.1206C55.1696 84.8787 66.1625 85.168 73.3205 84.7938L75.2864 84.6877C75.9959 85.6155 76.3779 86.7594 76.5854 88.0789C77.0778 91.2116 76.5854 97.4519 78.1364 97.5714C79.2376 97.6563 79.3268 96.3388 79.3268 96.3388C79.3268 96.3388 79.224 97.7624 80.5443 97.7643C80.9197 97.7785 81.2869 97.6527 81.5739 97.4114C81.8608 97.1702 82.0468 96.831 82.0954 96.4603C82.0954 96.4603 82.2679 98.3045 83.3653 97.5946C84.1815 97.0661 86.0427 91.0939 87.8691 84.5758C93.191 85.0503 96.8495 84.9616 97.9895 87.7567C99.9283 92.5001 100.045 97.7701 101.285 97.7875C102.668 97.8145 102.761 96.3195 102.761 96.3195C102.761 96.3195 103.174 98.0267 104.277 97.9997C105.32 97.9746 105.762 96.0707 105.762 96.0707C105.762 96.0707 105.495 97.855 106.79 97.9707C107.813 98.0633 108.249 97.23 108.637 95.1139C109.025 93.0499 114.525 68.1311 112.872 60.7643C112.782 59.9927 112.659 59.2449 112.501 58.5209C116.136 56.426 124.374 50.9978 129.894 42.4659C133.219 37.3675 138.841 24.0035 134.297 23.2994Z"></path></svg>
          </div>
        </div>
      </div>
      <div class="col">
        <div class="row">
          <div class="col">
            <label>Select image file</label>
            <input type="file" id="image-file" name="image" class="form-control mt-2" accept="image/png, image/jpeg" required>
          </div>
        </div>
        <div class="row mt-3">
          <div class="col">
            <div class="form-group">
              <label>Blur method</label>
              <select id="blur-method" name="typeBlur" class="form-control mt-2">
                <option value="1">Average Blur</option>
                <option value="2">Gaussian Blur</option>
                <option value="3">Median Blur</option>
                <option value="4">8-bit Blur</option>
                <option value="5">Bilateral Blur</option>
                <option value="6">Replace by Image</option>
              </select>
            </div>
          </div>
          <div class="col">
            <div class="form-group">
              <label>Model</label>
              <select class="form-control mt-2" disabled>
                <option value="1">YOLOv5</option>
                <option value="2">Detectron2</option>
              </select>
            </div>
          </div>
        </div>
        <div class="row mt-3">
          <div id="slide-of-size" class="col">
            <label class="form-label">Size of kernel:</label>
            <output>15</output>
            <input type="range" name="kernelSize" class="form-range" min="1" max="101" value="15" step="2" oninput="this.previousElementSibling.value=this.value">
          </div>
          <div id="slide-of-depth" class="col" style="display: none;">
            <label class="form-label">Depth:</label>
            <output>4</output>
            <input type="range" name="kernelDepth" class="form-range" min="1" max="15" value="4" oninput="this.previousElementSibling.value=this.value">
          </div>
        </div>
		<div id="image-replace" class="row" style="display: none;">
          <div class="col">
            <label>Select image replace file</label>
            <input type="file" name="imageReplace" class="form-control mt-2" accept="image/png, image/jpeg">
          </div>
        </div>
        <!-- <div class="row mt-3"> -->
          <!-- <div class="col"> -->
            <!-- <label class="form-label">Confidence:</label> -->
            <!-- <output>0.6</output> -->
            <!-- <input type="range" class="form-range" min="10" max="90" value="60" oninput="this.previousElementSibling.value=this.value / 100"> -->
          <!-- </div> -->
        <!-- </div> -->
        <div class="row mt-3">
          <div class="col text-center">
            <button type="submit" name="submit" class="btn btn-secondary">Detecting and Bluring</button>
          </div>
        </div>
      </div>
    </div>
  </form>
	<div class="footer">
		&copy; 2021 - Team: 
		<a href="https://github.com/lphuong304">19520227</a> -
		<a href="https://github.com/nhalq">19520195</a> -
		<a href="https://github.com/caohungphu">19520214</a>
	</div>
  <script>
    $("#image-file").change((e) => {
      let target = e.target || window.event.srcElement;
      let files = target.files;

      if (FileReader && files && files.length) {
        let reader = new FileReader();
        reader.onload = () => {
          $("#cat").hide();
          $("#image").show();
          document.getElementById("image").src = reader.result;
        }

        reader.readAsDataURL(files[0]);
      } else {
        $("#cat").show();
        $("#image").hide();
      }
    });

    $("#blur-method").change((e) => {
		if ($("#blur-method").val() == 6) {
		
			$("#image-replace").show();
			$("#slide-of-size").hide();
			$("#slide-of-depth").hide();
		} else {
			$("#image-replace").hide();
			$("#slide-of-size").show();
			if ($("#blur-method").val() == 4) {
				$("#slide-of-depth").show();
			} else {
				$("#slide-of-depth").hide();
			}
		}
    });
  </script>
</body>
</html>