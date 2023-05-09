using System.Collections;
using System.Collections.Generic;
using UnityEngine;

// INFO: i prefere to have the info from where the lib is used 
//using static UnityEngine.Mathf;


public delegate float TypeWaveFuncion1D(float u, float v, float t);
public delegate Vector3 TypeWaveFuncion3D(float u, float v, float t);
static public class FunctionLibrary 
{
    public enum EWAVE
    {
        SINGLE,
        MULTI,
        RIPPLE,
        SPHERE,
        THORUS
    };

    static float FACTOR_TRANSP = 1f / 2.5f;

    static public float Wave1D(float u, float v, float t)
    {
        float toReturn;

        
        toReturn = u + v + t;
        toReturn *= Mathf.PI;
        toReturn = Mathf.Sin(toReturn);
       
        return toReturn;
    }

    static public Vector3 Wave3D(float u, float v, float t)
    {
        Vector3 toReturn;

        toReturn.x = u;
        toReturn.y = Wave1D(u, v, t);
        toReturn.z = v;
        return toReturn;
    }

    static public float MultiWave1D(float u, float v, float t)
    {
        float toReturn;
        float firstWave;
        float secondWave;
        float thirdWave;
        

        firstWave = u + t;
        firstWave *= Mathf.PI;
        firstWave = Mathf.Sin(firstWave);

        secondWave = v + t;
        secondWave *= Mathf.PI * 2;
        secondWave = Mathf.Sin(secondWave) * 0.5f;


        thirdWave = Mathf.Sin(Mathf.PI * (u + v + 0.25f * t));

        // INFO: -1 < firstWave < 1
        // INFO: -0.5 < toReturn < 0.5
        toReturn = secondWave + firstWave + thirdWave;
        toReturn *= FACTOR_TRANSP;
        return toReturn;
    }

    static public Vector3 MultiWave3D(float u, float v, float t)
    {
        Vector3 toReturn;

        toReturn.x = u;
        toReturn.y = MultiWave1D(u, v, t);
        toReturn.z = v;
        return toReturn;
    }

    static public float Ripple1D(float u, float v, float t)
    {
        float toReturn;
        float d = Mathf.Sqrt(u * u + v * v);
        float y = Mathf.Sin(Mathf.PI * 4f * (d - t));

        // INFO: augment the ripple effect for better visibility
        toReturn = y / (1f + 10f * d);
        return toReturn;
    }

    static public Vector3 Ripple3D(float u, float v, float t)
    {
        Vector3 toReturn;

        toReturn.x = u;
        toReturn.y = Ripple1D(u, v, t);
        toReturn.z = v;
        return toReturn;
    }


    // INFO: not defined
    static public float Sphere1D(float u, float v, float t)
    {
        float toReturn = 0;
        
        return toReturn;
    }

    static public Vector3 Sphere3D(float u, float v, float t)
    {
        Vector3 toReturn;
        // INFO: uniform radius
        //float r = Mathf.Cos(0.5f * Mathf.PI * t);
        // INFO: rotating twisted sphere
        float r = 0.9f + 0.1f * Mathf.Sin(Mathf.PI * (6f * u + 4f * v + t));
        float s = r * Mathf.Cos(0.5f * Mathf.PI * v);

        toReturn.x = s * Mathf.Sin(Mathf.PI * u);
        toReturn.y = r * Mathf.Sin(Mathf.PI * 0.5f * v);
        toReturn.z = s * Mathf.Cos(Mathf.PI * u);
        return toReturn;
    }

    // INFO: not defined
    static public float Thorus1D(float u, float v, float t)
    {
        float toReturn = 0;

        return toReturn;
    }

    static public Vector3 Thorus3D(float u, float v, float t)
    {
        Vector3 toReturn;
        float r1 = 0.7f + 0.1f * Mathf.Sin(Mathf.PI * (6f * u + 0.5f * t));
        float r2 = 0.15f + 0.05f * Mathf.Sin(Mathf.PI * (8f * u + 4f * v + 2f * t));
        float s = r1 + r2 * Mathf.Cos(Mathf.PI * v);

        toReturn.x = s * Mathf.Sin(Mathf.PI * u);
        toReturn.y = r2 * Mathf.Sin(Mathf.PI * v);
        toReturn.z = s * Mathf.Cos(Mathf.PI * u);        
        return toReturn;
    }

    static TypeWaveFuncion1D[] _functions1D = { Wave1D, MultiWave1D, Ripple1D, Sphere1D, Thorus1D };
    public static TypeWaveFuncion1D GetFunction1D(EWAVE name)
    {
        return _functions1D[(int)name];
    }

    static TypeWaveFuncion3D[] _functions3D = { Wave3D, MultiWave3D, Ripple3D, Sphere3D, Thorus3D };
    public static TypeWaveFuncion3D GetFunction3D(EWAVE name)
    {
        return _functions3D[(int)name];
    }

}
