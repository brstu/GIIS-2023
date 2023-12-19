using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class EnemyBomber : EnemyAirPatrol
{
    [SerializeField] private GameObject prefabBullet;
    [SerializeField] private float timeShoot = 4f;
    private List<GameObject> bullet;
    private byte bulletNumber = 0;
    
    void Start()
    {
        bullet = new List<GameObject>();

        for (int i = 0; i < 2; i++)
        {
            bullet.Add(Instantiate(prefabBullet, transform.position, transform.rotation));
            bullet[i].SetActive(false);
        }

        StartCoroutine(Shooting());
    }

    IEnumerator Shooting()
    {
        yield return new WaitForSeconds(timeShoot);

        bullet[bulletNumber].transform.position = transform.position;
        bullet[bulletNumber].SetActive(true);

        if (bulletNumber == 3)
        {
            bulletNumber = 0;
        }

        StartCoroutine(Shooting());
    }
}
