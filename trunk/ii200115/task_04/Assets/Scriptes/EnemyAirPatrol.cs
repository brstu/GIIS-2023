using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class EnemyAirPatrol : Enemy
{
    [SerializeField] private float speed = 1.5f;
    [SerializeField] private Transform[] points;
    private byte i = 0;

    private float waitTime = 2f;
    private bool canGo = true;

    void Start()
    {
        gameObject.transform.position = new Vector3(points[i].position.x, transform.position.y, transform.position.z);
    }

    void Update()
    {
        if (canGo)
        {
            transform.position = Vector3.MoveTowards(transform.position, points[i].position, speed * Time.deltaTime);
        } 

        if (transform.position == points[i].position)
        {
            if (i < points.Length - 1)
            {
                i++;
            }
            else
            {
                i = 0;
            }

            canGo = false;
            StartCoroutine(Waiting());
        }
    }

    private IEnumerator Waiting()
    {
        yield return new WaitForSeconds(waitTime);

        byte point = (i - 1 > -1) ? (byte) (i - 1) : (byte) (points.Length - 1); 

        transform.eulerAngles = (points[point].transform.position.x < points[i].transform.position.x) ? new Vector3(0, 180, 0) : new Vector3(0, 0, 0);

        canGo = true;   
    }
}
