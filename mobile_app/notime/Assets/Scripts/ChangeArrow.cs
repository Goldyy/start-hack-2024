using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class ChangeArrow : MonoBehaviour
{
    public Transform arrow;

    // Update is called once per frame
    void Update()
    {
        arrow.position = this.transform.position;
        arrow.eulerAngles = new Vector3(arrow.eulerAngles.x, this.transform.eulerAngles.y, arrow.eulerAngles.z);
    }
}