using UnityEngine;

public class Destroyable : MonoBehaviour
{
    private void OnCollisionEnter2D(Collision2D other)
    {
        if (other.gameObject.tag == "Player")
        {
           other.gameObject.GetComponent<Rigidbody2D>().AddForce(transform.up * 8f, ForceMode2D.Impulse);
           gameObject.GetComponentInParent<Enemy>().StartCorutineDeath();
        }
    }
}
