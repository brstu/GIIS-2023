using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Finish : MonoBehaviour
{
    [SerializeField] private Main main;
    [SerializeField] private Sprite finSprite;
    
    private void OnTriggerEnter2D(Collider2D other) 
    {
        if (other.gameObject.tag == "Player")
        {
            GetComponent<SpriteRenderer>().sprite = finSprite;
            main.Win();
        }
    }
}
