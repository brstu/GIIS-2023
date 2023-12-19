using UnityEngine;

public class Door : MonoBehaviour
{
    public bool isOpen{get; private set;} = false;

    [SerializeField] private Transform door;
    [SerializeField] private Sprite mid, top;

    public void Unlock()
    {
        isOpen = true;

        transform.GetChild(0).GetComponent<SpriteRenderer>().sprite = mid;
        transform.GetChild(1).GetComponent<SpriteRenderer>().sprite = top;
    }

    public void Teleport(GameObject player)
    {
        player.transform.position = new Vector3(door.transform.position.x, door.transform.position.y, player.transform.position.z);
    }
}
