using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Btn : MonoBehaviour
{
    [SerializeField] private GameObject[] block;
    [SerializeField] private Sprite btnDown;

    private void OnCollisionEnter2D(Collision2D other)
    {
        if (other.gameObject.tag == "MarkBox")
        {
            GetComponent<SpriteRenderer>().sprite = btnDown;
            GetComponent<CircleCollider2D>().enabled = false;

            foreach (GameObject b in block)
            {
                Destroy(b);
            }
        }
    }
}
