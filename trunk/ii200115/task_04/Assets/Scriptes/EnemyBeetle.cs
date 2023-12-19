using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class EnemyBeetle : Enemy
{
    [SerializeField] private float waitTime = 4f;
    [SerializeField] private float speed = 4f;
    [SerializeField] private Transform point;
    private bool isWait = false;
    private bool isHidden = false;

    void Start()
    {
        point.transform.position = new Vector3(transform.position.x, transform.position.y + 1.25f, transform.position.z);
    }

    void Update()
    {
        if (!isWait)
        {
            transform.position = Vector3.MoveTowards(transform.position, point.position, speed * Time.deltaTime);
        }

        if (transform.position == point.position)
        {
            if (isHidden)
            {
                point.transform.position = new Vector3(transform.position.x, transform.position.y + 1.25f, transform.position.z);
                isHidden = false;
            }
            else
            {
                point.transform.position = new Vector3(transform.position.x, transform.position.y - 1.25f, transform.position.z);
                isHidden = true;
            }

            isWait = true;
            StartCoroutine(Waiting());
        }
    }

    private IEnumerator Waiting()
    {
        yield return new WaitForSeconds(waitTime);
        isWait = false;
    }
}
