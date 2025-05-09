'use client';

import { useState } from 'react';
import PlayerSearch from '@/components/PlayerSearch';
import PlayerCard from '@/components/PlayerCard';
import { PlayerSummary } from '@/lib/api';

export default function Home() {
  const [player, setPlayer] = useState<PlayerSummary | null>(null);

  return (
    <main className="min-h-screen bg-gray-50 py-12 px-4">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-4xl font-bold text-center mb-8">
          Basketball Player Comparison
        </h1>
        
        <div className="mb-8">
          <PlayerSearch onPlayerFound={setPlayer} />
        </div>

        {player && (
          <div className="mt-8">
            <PlayerCard player={player} />
          </div>
        )}

        {!player && (
          <div className="text-center text-gray-500 mt-12">
            <p>Search for a player to see their stats and summary</p>
          </div>
        )}
      </div>
    </main>
  );
}
