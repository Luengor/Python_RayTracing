# A very crude implementataion of RayTracing in Python
I literally have no idea what I am doing. I just hit my keyboard until something works :)
   
The idea is to (eventually) use the numba library to execute most of the code from the gpu. That way I can hide my bad coding abilities with the power ___of parallel computing___.
   
### This is what I have for now (2022-03-10):
<img title="Took 19.0 seconds to render" src="out/directional_lights.png" width="640" height="360">
<br><br>

### TODO:
* ~~Diffuse and Specular shading~~
* ~~Better~~ ~~Fix~~ Better shadows
* More primitives (Box, finite plane...)
* ~~Optimization~~
* ~~Scene class~~
*  ___Numba___   

### Maybe...?
* Anti-aliasing
* Model support
<br><br>

### Also, I am using/used this:  
https://tavianator.com/index.html  
https://www.scratchapixel.com/index.php  
http://lousodrome.net/blog/light/2020/07/03/intersection-of-a-ray-and-a-plane/
https://www.cs.cornell.edu/courses/cs4620/2017sp/slides/05rt-shading.pdf
