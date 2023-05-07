using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Graph : MonoBehaviour
{

    [SerializeField]
    Transform _pointPrefab;

    [SerializeField, Range(10, 100)]
    int _resolution = 10;    

    [SerializeField]
    float _scale = 0.001f;

    Transform[] _pointArray;
    float _step;

    void InitialiseData()
    {
        Vector3 scale = Vector3.one * _scale;
        Transform point;

        _step = 1f / (float)_resolution;
        _pointArray = new Transform[_resolution];
        for (int i = 0; i < _resolution; i++)
        {
            point = Instantiate(_pointPrefab);
           


            point.localScale = scale;
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


    float GetPositionX(int i)
    {
        float toReturn = (float)i * _step; ;

        //// INFO: transpose to the domain (-1 1)
        toReturn -= 0.5f;
        toReturn *= 2f;
        return toReturn;

    }
    // Update is called once per frame
    void Update()
    {
        Vector3 position = Vector3.zero;
        float time = Time.time;

        for (int i = 0; i < _resolution; i++)
        {
            Transform point = _pointArray[i];

            //// INFO: set the position between (0 ... 1)
            position.x = GetPositionX(i);
            position.y = Mathf.Sin(Mathf.PI * (position.x + time));

            point.localPosition = position;
        }
    }
}
