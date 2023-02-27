// Using to calculate color for each pixel

#version 330 core

#define MAX_ITERATIONS 2000

uniform vec2  iMouse; // never used
uniform float iTime;
uniform vec2  iResolution; // Size of the screen in pixels

uniform float CenterX;
uniform float CenterY;
uniform float ZoomScale;
uniform vec4 ColorRanges;

// Get variables from Python
in vec4 gl_FragCoord;
out vec4 frag_color;
out float frag_depth;

int GetIterations()
{
// calculates the number of iterations required to
// determine the color of a given pixel in the Mandelbrot fractal. The function
// takes no arguments and returns an integer value representing the number of
// iterations required.
    // if you change the screen , change the value of offset X and offset Y till it the mandelbrot is centered on your screen
    float offsetX = 1.0f;
    float offsetY = 0.5f;
    // divide by 1080 for make resolution independent. put (0, 0) coordinates on screen center
    // 4.0 set the maximum y and x
    // Offset for centered fractal on the screen
    // (gl_FragCoord.x and gl_FragCoord.y) -- cureen pixel coordinates
    float real = ((gl_FragCoord.x / 1080.0 - offsetX) * ZoomScale + CenterX )* 4.0;
    float imag = ((gl_FragCoord.y / 1080.0 - offsetY) * ZoomScale + CenterY )* 4.0;

    int iterations = 0;
    float real_number = real;
    float imaginary = imag;

    // Calculate fractal
    while (iterations < MAX_ITERATIONS)
    {
        // z = z^2 + c
        float tmp_real = real;
        real = (pow(real, 2) - pow(imag, 2)) + real_number;
        imag = (2.0 * tmp_real * imag) + imaginary;

        float dist = pow(real, 2) + pow(imag, 2);

        // prevent infinite iteration
        // This threshold is used as an escape condition for the loop that iteratively
        // calculates the number of iterations required to determine the color of the
        // current pixel. If the distance threshold is exceeded, the loop breaks and the
        // function returns the number of iterations performed up to that point. This
        // indicates that the current pixel is not part of the fractal and has "escaped"
        // to infinity.
        if (dist > 4.0){
            break;
        }

        ++iterations;
    }
    return iterations;
}

vec4 GetColorValues()
{
    vec2 uv = gl_FragCoord.xy/iResolution.xy * 2.0 - 1.0;
    uv.x *= iResolution.x / iResolution.y;

    int iter = GetIterations();
    if (iter == MAX_ITERATIONS)
    {
        gl_FragDepth = 0.0f;
        return vec4(0.001f, 0.00f, 0.001f, 1.0f);
    }

    float iterations = float(iter) / MAX_ITERATIONS;
    gl_FragDepth = iterations;

    vec3 iColor = 0.5 + 0.5 * cos(iTime + uv.xyx + vec3(0.0, 2.0, 4.0));
    vec4 color_0 = vec4(0.0f, 0.0f, 0.0f, 1.0f);
    vec4 color_1 = vec4(iColor.x/2, 0.5f, 0.6f, 1.0f);
    vec4 color_2 = vec4(0.3f, iColor.y, 0.4f, 1.0f);
    vec4 color_3 = vec4(iColor, 1.0f);

    float fraction = 0.0f;

    // Linearly interpolate between the four given colors.
    // The "mix" function takes in two colors and a "fraction" value,
    // and returns a color that is a linear blend between the two input colors
    // based on the fraction value.
    if (iterations < ColorRanges[1])
    {
        fraction = (iterations - ColorRanges[0]) / (ColorRanges[1] - ColorRanges[0]);
        return mix(color_0, color_1, fraction);
    }
    else if(iterations < ColorRanges[2])
    {
        fraction = (iterations - ColorRanges[1]) / (ColorRanges[2] - ColorRanges[1]);
        return mix(color_1, color_2, fraction);
    }
    else
    {
        fraction = (iterations - ColorRanges[2]) / (ColorRanges[3] - ColorRanges[2]);
        return mix(color_2, color_3, fraction);
    }
}

void main()
{
    // for just black and white:
    // float iter = GetIterations() / MAX_ITERATIONS;
    // vec3 col = vec3(iter);
    // frag_color = vec4(col, 1.0);

    vec4 color = GetColorValues();
    frag_color = color;
}
