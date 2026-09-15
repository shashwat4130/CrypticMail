import React from 'react';
import { Terminal } from 'lucide-react';

export default function Analysis() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold tracking-tight text-white">Stream Analysis</h1>
        <p className="text-sm text-gray-400 mt-1">
          Reconstructed TCP email flows, handshake telemetry, and state machine tracking.
        </p>
      </div>

      <div className="border border-gray-800 bg-gray-950/60 rounded-xl p-12 text-center">
        <Terminal className="w-8 h-8 text-gray-600 mx-auto mb-3" />
        <p className="text-sm text-gray-300">No session telemetry loaded</p>
        <p className="text-xs text-gray-500 mt-1 font-mono">
          Upload and process a capture file to inspect reconstructed TCP sessions.
        </p>
      </div>
    </div>
  );
}