using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Bullet : MonoBehaviour
{
    private float timeToDisable = 8f;
    private float speed = 3f;
    
    void Start()
    {
        StartCoroutine(SetDisabled());
    }
    
    void Update()
    {
        transform.Translate(Vector2.down * speed * Time.deltaTime);
    }

    private IEnumerator SetDisabled()
    {
        yield return new WaitForSeconds(timeToDisable);
        gameObject.SetActive(false);
    }

    private void OnCollisionEnter2D(Collision2D other)
    {
        StopCoroutine(SetDisabled());
        gameObject.SetActive(false);
    }
}
