using System.Collections;
using UnityEngine;

public class Enemy : MonoBehaviour
{
    private bool isHit = false;

    private void OnCollisionEnter2D(Collision2D other)
    {
        if (other.gameObject.tag == "Player" && !isHit)
        {
           other.gameObject.GetComponent<Player>().RecountHp(-1);
           other.gameObject.GetComponent<Rigidbody2D>().AddForce(transform.up * 8f, ForceMode2D.Impulse);
        }
    }

    private IEnumerator Death()
    {
        isHit = true;

        GetComponent<Animator>().SetBool("dead", true);
        GetComponent<Rigidbody2D>().bodyType = RigidbodyType2D.Dynamic;
        GetComponent<Collider2D>().enabled = false;
        GetComponentInChildren<Collider2D>().enabled = false;

        yield return new WaitForSeconds(2f);
        Destroy(gameObject);
    }

    public void StartCorutineDeath()
    {
        StartCoroutine(Death());
    }
}
