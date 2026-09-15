import React from 'react';
import { UploadCloud, Layers, FileCheck, Lock } from 'lucide-react';

export default function Home() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold tracking-tight text-white">Capture Ingestion</h1>
        <p className="text-sm text-gray-400 mt-1">
          Forensic intake for PCAP/PCAPNG network packet captures containing email communications.
        </p>
      </div>

      {/* Visual-only upload area - No file handling attached */}
      <div className="border border-dashed border-gray-800 hover:border-gray-700 bg-gray-950/60 rounded-xl p-12 text-center transition-all">
        <div className="max-w-md mx-auto space-y-4">
          <div className="w-12 h-12 rounded-xl bg-blue-600/10 border border-blue-500/20 text-blue-400 flex items-center justify-center mx-auto">
            <UploadCloud className="w-6 h-6" />
          </div>
          <div>
            <h3 className="text-base font-semibold text-white">Select Network Capture File</h3>
            <p className="text-xs text-gray-400 mt-1">
              Supports standard <code>.pcap</code> and <code>.pcapng</code> captures.
            </p>
          </div>
          <div className="pt-2">
            <button
              type="button"
              className="px-4 py-2 text-sm font-medium rounded-lg bg-blue-600/50 text-gray-300 cursor-not-allowed border border-blue-500/30"
              disabled
            >
              PCAP Ingestion Available in Step 6
            </button>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 pt-4">
        <div className="border border-gray-800 bg-gray-900/40 p-4 rounded-lg space-y-2">
          <div className="flex items-center gap-2 text-blue-400 text-sm font-medium">
            <Layers className="w-4 h-4" />
            <span>Dual-Mode Detection</span>
          </div>
          <p className="text-xs text-gray-400">
            Monitors explicit STARTTLS (Ports 25, 587) and direct implicit TLS (Ports 465, 993, 995).
          </p>
        </div>
        <div className="border border-gray-800 bg-gray-900/40 p-4 rounded-lg space-y-2">
          <div className="flex items-center gap-2 text-emerald-400 text-sm font-medium">
            <FileCheck className="w-4 h-4" />
            <span>Deterministic Rules</span>
          </div>
          <p className="text-xs text-gray-400">
            Audits protocol parameters against NIST SP 800-52r2 and RFC 8996 compliance standards.
          </p>
        </div>
        <div className="border border-gray-800 bg-gray-900/40 p-4 rounded-lg space-y-2">
          <div className="flex items-center gap-2 text-purple-400 text-sm font-medium">
            <Lock className="w-4 h-4" />
            <span>Zero-Payload Inspection</span>
          </div>
          <p className="text-xs text-gray-400">
            Audits handshakes and cryptographic headers passively without reading email messages.
          </p>
        </div>
      </div>
    </div>
  );
}