using System;
using System.Collections.Generic;
using Unity.VisualScripting;
using UnityEngine;


[System.Serializable]
public class PlayerData
{
    public int id;
    public int @class;
    public float x;
    public float z;
}

[System.Serializable]
public class FramePacket
{
    public List<PlayerData> players;
}


public class PlayerPlacing : MonoBehaviour
{
    public GameObject playerPrefab; 
    public GameObject ballPrefab;   

    private Dictionary<int, GameObject> activeEntities = new Dictionary<int, GameObject>();
    private Dictionary<int, float> lastSeenTime = new Dictionary<int, float>();
    
    public float timeoutDuration = 1.0f; 
    public float scaleFactor = 0.02f;
    public Vector3 offset = new Vector3(-10, 0, 5);

    public void ProcessFrame(FramePacket packet)
    {
        if (packet == null || packet.players == null) return;

        // Process all Players
        foreach (PlayerData p in packet.players)
        {
            // Does it exist
            if (!activeEntities.ContainsKey(p.id))
            {
                GameObject prefabToUse = (p.@class == 32) ? ballPrefab : playerPrefab;
                if (prefabToUse == null) prefabToUse = playerPrefab;

                GameObject newObj = Instantiate(prefabToUse);
                newObj.name = "ID_" + p.id;
                activeEntities.Add(p.id, newObj);
            }

            // Pos update
            float xPos = p.x * scaleFactor + offset.x;
            float zPos = -p.z * scaleFactor + offset.z;
            activeEntities[p.id].transform.position = new Vector3(xPos, 0.5f, zPos);

            
            lastSeenTime[p.id] = Time.time;
        }

        CleanupOldIDs();
    }

    private void CleanupOldIDs()
    {
        List<int> idsToRemove = new List<int>();

        foreach (var entry in lastSeenTime)
        {
            if (Time.time - entry.Value > timeoutDuration)
            {
                idsToRemove.Add(entry.Key);
            }
        }

        foreach (int id in idsToRemove)
        {
            if (activeEntities.ContainsKey(id))
            {
                Destroy(activeEntities[id]); 
                activeEntities.Remove(id);    
            }
            lastSeenTime.Remove(id);         
        }
    }
}