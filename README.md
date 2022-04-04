# A very crude implementataion of RayTracing in Python
I literally have no idea what I am doing. I just hit my keyboard until something works :)
   
The idea is to (eventually) use the numba / taichi / multiprocessing library so I can hide my bad coding abilities with the power of ___parallel computing___.
   
### This is what I have for now (15-03-2022):
<img title="Took <a long time> to render" src="out/SSAA.png" width="640" height="360">
<br><br>

### Dependencies
Package       | Version
--------------|----------
python        | 3.10.3
opencv-python | 4.5.5.64
numpy         | 1.22.3
<br>

### TODO:
* ~~Diffuse and Specular shading~~
* ~~Better~~ ~~Fix~~ Better shadows
* More primitives (Box, finite plane...)
* ~~Optimization~~
* ~~Scene class~~
*  ___Numba___ / ___Taichi___ / _multiprocessing_

### Maybe...?
* ~~Anti-aliasing~~
* Model support
<br><br>

### Also, I am using/used this:  
https://tavianator.com/index.html  
https://www.scratchapixel.com/index.php  
http://lousodrome.net/blog/light/2020/07/03/intersection-of-a-ray-and-a-plane/
https://www.cs.cornell.edu/courses/cs4620/2017sp/slides/05rt-shading.pdf
