'use client';

import { PlayerSummary } from '@/lib/api';

interface PlayerCardProps {
  player: PlayerSummary;
}

export default function PlayerCard({ player }: PlayerCardProps) {
  return (
    <div className="p-6 bg-white rounded-lg shadow-md">
      <h2 className="text-2xl font-bold mb-4">{player.name}</h2>
      
      <div className="prose max-w-none mb-6">
        <p className="text-gray-700">{player.summary}</p>
      </div>

      {player.stats && (
        <div className="mt-4">
          <h3 className="text-lg font-semibold mb-2">Season Stats</h3>
          <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
            {Object.entries(player.stats).map(([key, value]) => (
              <div key={key} className="bg-gray-50 p-3 rounded">
                <div className="text-sm text-gray-500 capitalize">{key.replace(/_/g, ' ')}</div>
                <div className="font-medium">{value}</div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
} 