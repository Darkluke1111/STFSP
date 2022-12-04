//author: Darkluke1111 (https://www.nexusmods.com/users/8086919)
//based on the ml-parallax shader of nifscope


import lib-sparse.glsl
import lib-sampler.glsl
import lib-env.glsl
import lib-random.glsl
import lib-defines.glsl
import lib-vectors.glsl

// -- Initialize Properties from Substance Painter --
//: param auto world_eye_position
uniform vec3 world_eye_position;
//: param auto camera_view_matrix
uniform mat4 view_matrix;
//: param auto camera_view_matrix_it
uniform mat4 view_matrix_it;

// -- Initialize Texture Channels from Substance Painter --
//: param auto channel_diffuse
uniform SamplerSparse diffuse_tex;
//: param auto channel_normal
uniform SamplerSparse normal_tex;
//: param auto channel_height
uniform SamplerSparse height_tex;
//: param auto channel_emissive
uniform SamplerSparse glow_tex;
//: param auto channel_specularlevel
uniform SamplerSparse spec_tex;
//: param auto channel_opacity
uniform SamplerSparse opacity_tex;
//: param auto channel_reflection
uniform SamplerSparse envMap_tex;

// -- Specular --
//: param custom {"visible": false, "default": true,"label": "Enable Specular Map", "group": "BSLightingShader Parameters/Specular"}
uniform bool specMapEnabled;

//: param custom { 
//:     "default": [0.0,0.0,0.0], 
//:     "label": "Specular Color", 
//:     "widget": "color", 
//:     "group": "BSLightingShader Parameters/Specular",
//:     "description": "Specular Color"
//: }
uniform vec3 specColor;

//: param custom { 
//:     "default": 0.0, 
//:     "min": 0.0, 
//:     "max": 10.0, 
//:     "label": "Specular Strength", 
//:     "group": "BSLightingShader Parameters/Specular",
//:     "description": "Increases/Decreases strength of specular highlight"
//: }
uniform float specStrength;

//: param custom { 
//:     "default": 0.0, 
//:     "min": 0.0, 
//:     "max": 1000.0, 
//:     "label": "Specular Glossiness", 
//:     "group": "BSLightingShader Parameters/Specular",
//:     "description": "Increases/Decreases falloff of specular highlight"
//: }
uniform float specGlossiness;

// -- Multi Layer Parallax --
//: param custom { 
//:     "default": 1.0, 
//:     "label": "Outer Refection Strength", 
//:     "group": "Multi Layer Parallax",
//:     "description": "Outer Refection Strength"
//: }
uniform float outerRefraction;

//: param custom { 
//:     "default": "", 
//:     "default_color": [1.0, 1.0, 0.0, 1.0], 
//:     "label": "Inner Texture", 
//:     "usage": "texture" 
//:     }
uniform sampler2D inner_tex;

//: param custom { 
//:     "default": [1.0,1.0], 
//:     "label": "Inner Scale", 
//:     "group": "Multi Layer Parallax",
//:     "description": "Defined Inner Texture Tiling"
//: }
uniform vec2 innerScale;

//: param custom { 
//:     "default": 1.0, 
//:     "min": 0.0,
//:     "max": 1000.0,
//:     "label": "Inner Thickness", 
//:     "group": "Multi Layer Parallax",
//:     "description": "Defined Inner Layer Thickness"
//: }
uniform float innerThickness;

// -- Glow --
//: param custom {
//:     "default": false,
//:     "label": "Enable Glow", 
//:     "group": "BSLightingShader Parameters/Glow",
//:     "description": "Enables/Disables the emissive shading."
//: }
uniform bool glowEnabled;

//: param custom {
//:     "default": true,
//:     "label": "Enable Glow Map", 
//:     "group": "BSLightingShader Parameters/Glow",
//:     "description": "Enables/Disables the glow map. If disabled the whole mesh will glow!"
//: }
uniform bool glowMapEnabled;

//: param custom { 
//:     "default": [0.0,0.0,0.0], 
//:     "label": "Emissive Color", 
//:     "widget": "color", 
//:     "group": "BSLightingShader Parameters/Glow" ,
//:     "description": "Glow Color"
//: }
uniform vec3 glowColor;

//: param custom { 
//:     "default": 0.0, 
//:     "min": 0.0, 
//:     "max": 100.0, 
//:     "label": "Emissive Multiple", 
//:     "group": "BSLightingShader Parameters/Glow",
//:     "description": "Increases/Decreases the glow strength"
//: }
uniform float glowMult;

// -- Environment --
//: param custom {
//:     "visible": false, 
//:     "default": true,
//:     "label": "Enable Environment Mapping", 
//:     "group": "BSLightingShader Parameters/Environment",
//:     "description": "Increases/Decreases the environment reflection strength"
//: }

uniform bool envMapEnabled;
//: param custom { 
//:     "default": 1.0, 
//:     "min": 0.0, 
//:     "max": 10.0, 
//:     "label": "Environment Map Strength", 
//:     "group": "BSLightingShader Parameters/Environment",
//:     "description": "Increases/Decreases the glow strength"
//: }
uniform float envReflection;


// -- Lighting Constants --
//: param custom { 
//:     "default": false, 
//:     "label": "Enable Frontal Lighting", 
//:     "group": "NifScope Lighting Parameters",
//:     "description": "If enabled the light source will be bound to your camera position"
//: }
uniform bool frontal_lighting;

//: param custom { 
//:     "default": [0.0,100.0,0.0] , 
//:     "min": -100.0, "max": 100.0, 
//:     "label": "Light Position",
//:     "group": "NifScope Lighting Parameters",
//:     "description": "Sets the Position of the light (Has no effect when Fronatl Lighting is enabled)"
//: }
uniform vec3 world_lighting;

//: param custom { 
//:     "default": 0.5, 
//:     "min": 0.0, 
//:     "max": 1.0, 
//:     "label": "Ambient Light", 
//:     "group": "NifScope Lighting Parameters",
//:     "description": "Increases/Decreases ambient lighting"
//: }
uniform float A;

//: param custom { 
//:     "default": 0.5, 
//:     "min": 0.0, 
//:     "max": 1.0, 
//:     "label": "Diffuse Light", 
//:     "group": "NifScope Lighting Parameters",
//:     "description": "Increases/Decreases diffuse lighting"
//: }
uniform float D;

// Unused
//: param custom { "visible": false, "default": 1.0, "min": 0.0, "max": 1.0, "label": "Vertex Color" , "group": "NifScope Lighting Parameters"}
uniform float C;
//: param custom { "visible": false, "default": 1.0, "min": 0.0, "max": 1.0, "label": "Vertex Color alpha" , "group": "NifScope Lighting Parameters"}
uniform float Ca;


float normal_intensity = 2.0;

vec3 myGetTSNormal(SparseCoord coord)
{
  float height_force = 0.0;
  vec3 normalH = normalFromHeight(coord, height_force);
  return getTSNormal(coord, normalH);
}

vec3 myComputeWSNormal(SparseCoord coord, vec3 tangent, vec3 bitangent, vec3 normal)
{
  vec3 normal_vec = getTSNormal(coord) * vec3(1.0,normal_intensity,1.0);
  return normalize(
    normal_vec.x * tangent +
    normal_vec.y * bitangent +
    normal_vec.z * normal
  );
}

vec3 ParallaxOffsetAndDepth(vec2 tex_coord, vec2 vInnerScale, vec3 vViewTS, vec3 vNormalTS, float fLayerThickness )
{
	// Tangent space reflection vector
	vec3 vReflectionTS = reflect( -vViewTS, vNormalTS );
	// Tangent space transmission vector (reflect about surface plane)
	vec3 vTransTS = vec3( vReflectionTS.xy, -vReflectionTS.z );
	
	// Distance along transmission vector to intersect inner layer
	float fTransDist = fLayerThickness / abs(vTransTS.z);
	
	// Texel size
	// 	Bethesda's version does indeed seem to assume 1024, which is why they
	//	introduced the additional parameter.
	vec2 vTexelSize = vec2( 1.0/(1024.0 * vInnerScale.x), 1.0/(1024.0 * vInnerScale.y) );
	
	// Inner layer’s texture coordinate due to parallax
	vec2 vOffset = vTexelSize * fTransDist * vTransTS.xy;
	vec2 vOffsetTexCoord = tex_coord + vOffset;
	
	// Return offset texture coordinate in xy and transmission dist in z
	return vec3( vOffsetTexCoord, fTransDist );
}

vec3 tonemap(vec3 x)
{
	float _A = 0.15;
	float _B = 0.50;
	float _C = 0.10;
	float _D = 0.20;
	float _E = 0.02;
	float _F = 0.30;

	return ((x*(_A*x+_C*_B)+_D*_E)/(x*(_A*x+_B)+_D*_F))-_E/_F;
}

void shade(V2F inputs) { 
    
    vec3 N = normalize(inputs.normal); // Facenormal
    vec3 T = normalize(inputs.tangent); // Facetangent
    vec3 B = normalize(inputs.bitangent); // Facebitangent
    
    vec3 light_pos;
    if(frontal_lighting) {
        light_pos = world_eye_position;
    } else {
        light_pos = world_lighting;
    }
    vec3 camera_pos = world_eye_position;
    
    vec3 baseMap = getBaseColor(diffuse_tex, inputs.sparse_coord);
    vec3 normalMap = myComputeWSNormal(inputs.sparse_coord, T, B, N);
    vec4 innerMap = texture(inner_tex, inputs.sparse_coord.tex_coord);
    vec3 glowMap = getBaseColor(glow_tex, inputs.sparse_coord);
    float specMap = getSpecularLevel(spec_tex, inputs.sparse_coord);
    vec3 envMap =  getBaseColor(envMap_tex, inputs.sparse_coord);
    float alphaMap = getOpacity(opacity_tex, inputs.sparse_coord);
    
    float innerMapAlpha = innerMap.a;
    
    vec3 L = normalize(light_pos - inputs.position); //Light Directtion
    vec3 E = normalize(camera_pos - inputs.position); // View Direction
	vec3 H = normalize( L + E );
    
    vec3 normal = normalize(normalMap *  2 - 1);
    
	float NdotL = max( dot(normal, L), 0.0 );
	float NdotH = max( dot(normal, H), 0.0 );
	float EdotN = max( dot(normal, E), 0.0 );
    
    
    // Mix between the face normal and the normal map based on the refraction scale
	vec3 mixedNormal = mix( vec3(0.0, 0.0, 1.0), myGetTSNormal(inputs.sparse_coord), clamp( outerRefraction, 0.0, 1.0 ) );
	vec3 parallax = ParallaxOffsetAndDepth(inputs.sparse_coord.tex_coord, innerScale, worldSpaceToTangentSpace(E, inputs), mixedNormal, innerThickness * innerMapAlpha );
    
    // Sample the inner map at the offset coords
	innerMap = texture( inner_tex, parallax.xy * innerScale );
    
    // Calculate Reflection Direction
    vec3 reflected = reflect( -E, normal );
	vec3 reflectedVS = B * reflected.x + T * reflected.y + N * reflected.z;
    vec3 reflectedWS = vec3(view_matrix_it * vec4( reflectedVS, 0.0 ) );
    
    vec3 color;
	vec3 albedo;
	vec3 diffuse = vec3(A) + (D * NdotL);
	vec3 inner = innerMap.rgb * C;
	vec3 outer = baseMap * C;
    vec3 emissive =  vec3(0.0);
    vec3 spec = vec3(0.0);
    
    // Mix inner/outer layer based on fresnel
	float outerMix = max( 1.0 - EdotN, alphaMap );
	albedo = mix( inner, outer, outerMix );
    
    // Environment Reflections
    vec3 cube = envSampleLOD(normalize(reflected),1.0) * envIrradiance(normalize(reflectedWS));
    cube = cube * envMap.r * envReflection;
    albedo += cube;
    
    // Glow
    if(glowEnabled) {
        emissive += glowColor * glowMult;
        emissive *= (glowMapEnabled ? glowMap : vec3(1.0));
    }
    
    // Specular
	spec = clamp( specColor * specStrength * specMap * pow(NdotH, specGlossiness), 0.0, 1.0 );
	spec *= D;
    
    // Mixing
    color = albedo * (diffuse + emissive) + spec;
	color = tonemap( color ) / tonemap( vec3(1.0) );
    
    //specularShadingOutput(spec);
    diffuseShadingOutput(color);
}