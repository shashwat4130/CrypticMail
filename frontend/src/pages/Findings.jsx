import React from 'react';
import { ShieldAlert } from 'lucide-react';

export default function Findings() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold tracking-tight text-white">Findings</h1>
        <p className="text-sm text-gray-400 mt-1">
          Cryptographic non-compliance, deprecated algorithms, and protocol deviations.
        </p>
      </div>

      <div className="border border-gray-800 bg-gray-950/60 rounded-xl p-12 text-center">
        <ShieldAlert className="w-8 h-8 text-gray-600 mx-auto mb-3" />
        <p className="text-sm text-gray-300">No findings detected yet</p>
        <p className="text-xs text-gray-500 mt-1 font-mono">
          Deterministic and policy observations will be listed here after forensic parsing.
        </p>
      </div>
    </div>
  );
}