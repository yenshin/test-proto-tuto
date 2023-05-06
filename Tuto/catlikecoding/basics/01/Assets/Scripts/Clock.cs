using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Clock : MonoBehaviour
{
    #region Serialized fields
    [SerializeField]
    Transform _hoursPivot, _minutesPivot, _secondsPivot;


    #endregion

   
    const float _hoursToDegrees = -30;
    const float _minutesAndSecondsToDegrees = -6f;

    void DiscreteSetArmPosition()
    {
        DateTime actualTime = DateTime.Now;

        _hoursPivot.localRotation = Quaternion.Euler(0, 0, _hoursToDegrees * actualTime.Hour);
        _minutesPivot.localRotation = Quaternion.Euler(0, 0, _minutesAndSecondsToDegrees * actualTime.Minute);
        _secondsPivot.localRotation = Quaternion.Euler(0, 0, _minutesAndSecondsToDegrees * actualTime.Second);
    }

    void AnalogSetArmPosition()
    {
        DateTime actualTime = DateTime.Now;
        TimeSpan time = actualTime.TimeOfDay;
        _hoursPivot.localRotation = Quaternion.Euler(0, 0, _hoursToDegrees * (float)time.TotalHours);
        _minutesPivot.localRotation = Quaternion.Euler(0, 0, _minutesAndSecondsToDegrees * (float)time.TotalMinutes);
        _secondsPivot.localRotation = Quaternion.Euler(0, 0, _minutesAndSecondsToDegrees * (float)time.TotalSeconds);
    } 


    #region built in unity callback (awake start update)
    void Awake() 
    {
        AnalogSetArmPosition();
    }
    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        AnalogSetArmPosition();
    }
    #endregion
}
