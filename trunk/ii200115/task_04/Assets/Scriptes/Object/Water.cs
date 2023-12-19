using UnityEngine;

public class Water : MonoBehaviour
{
    private float time;

    private void Update()
    {
        time += Time.deltaTime;

        if (time >= 2f)
        {
            time = 0;
            transform.localScale = new Vector3(-1f, 1f, 1f);
        }
        else if (time >= 1f)
        {
            transform.localScale = new Vector3(1f, 1f, 1f);
        }
    }

    private void OnTriggerStay2D(Collider2D other)
    {
        if (other.gameObject.tag == "Player")
        {
            other.gameObject.GetComponent<Player>().InWater = true;
        }    
    }

    private void OnTriggerExit2D(Collider2D other)
    {
        if (other.gameObject.tag == "Player")
        {
            other.gameObject.GetComponent<Player>().InWater = false;
        }
    }
}
