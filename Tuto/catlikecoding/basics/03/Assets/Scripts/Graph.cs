using System.Collections;
using System.Collections.Generic;
using System.Reflection;
using UnityEngine;


public class Graph : MonoBehaviour
{




    [SerializeField]
    Transform _pointPrefab;

    const int C_RESOLUTION_MIN = 10;
    const int C_RESOLUTION_MAX = 100;
    [SerializeField, Range(C_RESOLUTION_MIN, 100)]
    int _resolution = C_RESOLUTION_MIN;    


    Transform[] _pointArray;
    float _step;

    [SerializeField, Range(0f, 1f)]
    float _timeFactor = 0.25f;

    [SerializeField]
    FunctionLibrary.EWAVE _waveId;


    int _lastResolution = 0;
    int _nbDot;
    int _maxDot;
    float _scaleF;
    Vector3 _scaleV3; 


    bool NeedUpdateBasicData()
    {
        bool toReturn = false;

        if (_lastResolution != _resolution)
        {
            _scaleF = 1f / _resolution;
            _scaleV3 = Vector3.one * _scaleF;
            _step = 1f / (float)_resolution;
            _nbDot = _resolution * _resolution;
            _lastResolution = _resolution;
            toReturn = true;
        }
        return toReturn;
    }
    void InitialiseData()
    {
        
        Transform point;

        NeedUpdateBasicData();
        _maxDot = C_RESOLUTION_MAX * C_RESOLUTION_MAX;
        _pointArray = new Transform[_maxDot];        
        for (int i = 0; i < _maxDot; ++i)
        {           
            point = Instantiate(_pointPrefab);                     
            point.SetParent(transform, false);
            _pointArray[i] = point;
        }

    }
    void Awake()
    {
        InitialiseData();                
    }

    // Start is called before the first frame update
    void Start()
    {
        
    }


    float GetPosition(int i)
    {
        float toReturn = (float)i * _step; ;

        //// INFO: transpose to the domain (-1 1)
        toReturn -= 0.5f;
        toReturn *= 2f;
        return toReturn;

    }


    void UpdateOneDot(Transform point,
                      float time,
                      ref float v,
                      ref int x,
                      ref int z)
    {
        float u;
        point.localScale = _scaleV3;
        if (x == _resolution)
        {
            x = 0;
            ++z;
            v = GetPosition(z);
        }

        //// INFO: set the position between (0 ... 1)
        u = GetPosition(x);

        point.localPosition = FunctionLibrary.GetFunction3D(_waveId)(u, v, time);
    }



    
    // Update is called once per frame
    void Update()
    {
        float time = Time.time * _timeFactor;
        float v = GetPosition(0);

        if (NeedUpdateBasicData())
        {            
            // INFO: hide  other dot by setting scale to zero
            for (int i = 0, x = 0, z = 0; i < _maxDot; ++i, ++x)
            {
                Transform point = _pointArray[i];

                if (i < _nbDot)
                {
                    UpdateOneDot(point, time, ref v, ref x, ref z);
                }
                else
                {
                    point.localScale = Vector3.zero;
                }
            }
        }
        else
        {      
            // INFO: avoid parsing all here
            for (int i = 0, x = 0, z = 0; i < _nbDot; ++i, ++x)
            {
                Transform point = _pointArray[i];

                UpdateOneDot(point, time, ref v, ref x, ref z);
            }
        }
        
    }
}
