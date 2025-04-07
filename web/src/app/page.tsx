"use client"

import Link from 'next/link'
import React, { useState, useEffect } from 'react';

export type Player = {
  name: string;
  description: string;
};

export default function Home() {
  const [players, setPlayers] = useState<Player[]>([]);
  const [playerName, setPlayerName] = useState('');

  const backend = 'http://127.0.0.1:8000';

  const addPlayer = async () => {
    const newPlayer: Player =
    {
      name: playerName,
      description: "loren ipsum"
    };

    const response = await fetch(`${backend}/addPlayer`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(newPlayer),
    });

    if (response.ok) {
      getPlayers();
      setPlayerName('');
    }
  };

  const getPlayers = async () => {
    const response = await fetch(`${backend}/players`);
    if (response.ok) {
      const data = await response.json();
      setPlayers(data);
    }
  };

  useEffect(() => {
    getPlayers();
  }, []);

  return (
    <div>

      <input type="text"
        value={playerName}
        onChange={(e) => setPlayerName(e.target.value)}
        placeholder="Enter player name" />
      <button onClick={addPlayer}>add Player</button>

      <ul>
        {players.map((player) => (
          <li key={player.name}>
            <Link href={`/player/${player.name}`}>{player.name}</Link>
          </li>
        ))}
      </ul>
      nba stas
    </div>
  );
}
