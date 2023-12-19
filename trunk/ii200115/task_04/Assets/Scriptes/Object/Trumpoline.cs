using System.Collections;
using UnityEngine;

public class Trumpoline : MonoBehaviour
{
    private void OnCollisionEnter2D(Collision2D other)
    {
        if (other.gameObject.tag == "Player")
        {
            StartCoroutine(TrampolineAnim(gameObject.GetComponent<Animator>()));
        }
    }

    private IEnumerator TrampolineAnim(Animator anim)
    {
        anim.SetBool("isJump", true);
        yield return new WaitForSeconds(0.3f);
        anim.SetBool("isJump", false);
    }
}
