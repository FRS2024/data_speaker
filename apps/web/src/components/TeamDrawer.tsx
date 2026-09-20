import React, { useState, useEffect } from "react";
import {
  X,
  Users,
  Building2,
  UserPlus,
  Shield,
  Trash2,
  LogOut,
  Check,
  Plus,
  ChevronRight,
  User as UserIcon,
} from "lucide-react";
import { authApi, workspacesApi, setActiveWorkspace } from "../lib/api";
import { User, Workspace, WorkspaceMember, WorkspaceRole } from "../lib/types";

interface TeamDrawerProps {
  isOpen: boolean;
  onClose: () => void;
  currentUser: User | null;
  activeWorkspace: Workspace | null;
  onWorkspaceChange: (ws: Workspace) => void;
  onOpenAuth: () => void;
}

export const TeamDrawer: React.FC<TeamDrawerProps> = ({
  isOpen,
  onClose,
  currentUser,
  activeWorkspace,
  onWorkspaceChange,
  onOpenAuth,
}) => {
  const [workspaces, setWorkspaces] = useState<Workspace[]>([]);
  const [members, setMembers] = useState<WorkspaceMember[]>([]);
  const [loadingMembers, setLoadingMembers] = useState(false);
  const [inviteEmail, setInviteEmail] = useState("");
  const [inviteRole, setInviteRole] = useState<WorkspaceRole>("analyst");
  const [newWsName, setNewWsName] = useState("");
  const [showNewWsInput, setShowNewWsInput] = useState(false);
  const [actionError, setActionError] = useState<string | null>(null);

  const isGuest = !currentUser || currentUser.id === "guest_usr";
  const userRole = activeWorkspace?.role || (isGuest ? "owner" : "analyst");
  const canManageTeam = userRole === "owner" || userRole === "admin";

  useEffect(() => {
    if (isOpen) {
      loadWorkspaces();
      if (activeWorkspace) {
        loadMembers(activeWorkspace.id);
      }
    }
  }, [isOpen, activeWorkspace?.id]);

  const loadWorkspaces = async () => {
    try {
      const list = await workspacesApi.list();
      setWorkspaces(list);
    } catch {
      // Fallback
    }
  };

  const loadMembers = async (wsId: string) => {
    setLoadingMembers(true);
    try {
      const list = await workspacesApi.listMembers(wsId);
      setMembers(list);
    } catch {
      setMembers([]);
    } finally {
      setLoadingMembers(false);
    }
  };

  const handleCreateWorkspace = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newWsName.trim()) return;
    setActionError(null);
    try {
      const ws = await workspacesApi.create(newWsName.trim());
      setNewWsName("");
      setShowNewWsInput(false);
      await loadWorkspaces();
      setActiveWorkspace(ws);
      onWorkspaceChange(ws);
    } catch (err: any) {
      setActionError(err.message || "Failed to create workspace");
    }
  };

  const handleInvite = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!activeWorkspace || !inviteEmail.trim()) return;
    setActionError(null);
    try {
      await workspacesApi.inviteMember(activeWorkspace.id, inviteEmail.trim(), inviteRole);
      setInviteEmail("");
      await loadMembers(activeWorkspace.id);
    } catch (err: any) {
      setActionError(err.message || "Failed to invite member");
    }
  };

  const handleUpdateRole = async (userId: string, newRole: string) => {
    if (!activeWorkspace) return;
    try {
      await workspacesApi.updateRole(activeWorkspace.id, userId, newRole);
      await loadMembers(activeWorkspace.id);
    } catch (err: any) {
      setActionError(err.message || "Failed to update role");
    }
  };

  const handleRemoveMember = async (userId: string) => {
    if (!activeWorkspace) return;
    try {
      await workspacesApi.removeMember(activeWorkspace.id, userId);
      await loadMembers(activeWorkspace.id);
    } catch (err: any) {
      setActionError(err.message || "Failed to remove member");
    }
  };

  const handleSignOut = async () => {
    await authApi.logout();
    onClose();
    window.location.reload();
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 overflow-hidden bg-black/60 backdrop-blur-sm animate-fade-in">
      <div className="absolute inset-0" onClick={onClose} />

      <div className="absolute inset-y-0 left-0 max-w-full flex pl-0 pr-10">
        <div className="relative w-screen max-w-md bg-slate-900 border-r border-slate-700/80 shadow-2xl flex flex-col">
          {/* Header */}
          <div className="p-6 border-b border-slate-800 flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-cyan-600 to-indigo-600 flex items-center justify-center text-white font-bold shadow-md shadow-indigo-600/20">
                {currentUser?.full_name ? currentUser.full_name[0].toUpperCase() : "G"}
              </div>
              <div>
                <h3 className="text-sm font-semibold text-white">
                  {currentUser?.full_name || "Guest Analyst"}
                </h3>
                <p className="text-xs text-slate-400 truncate max-w-[200px]">
                  {currentUser?.email || "guest@dataspkr.local"}
                </p>
              </div>
            </div>
            <button
              onClick={onClose}
              className="p-1.5 text-slate-400 hover:text-white rounded-lg hover:bg-slate-800 transition-colors"
            >
              <X className="w-5 h-5" />
            </button>
          </div>

          {/* Drawer Body */}
          <div className="flex-1 overflow-y-auto p-6 space-y-6">
            {/* Action error banner */}
            {actionError && (
              <div className="p-3 rounded-lg bg-rose-950/60 border border-rose-800 text-rose-300 text-xs flex items-center justify-between">
                <span>{actionError}</span>
                <button onClick={() => setActionError(null)} className="text-rose-400 hover:text-white">
                  <X className="w-3.5 h-3.5" />
                </button>
              </div>
            )}

            {/* Workspace Selector */}
            <div>
              <div className="flex items-center justify-between mb-3">
                <span className="text-xs font-semibold uppercase tracking-wider text-slate-400 flex items-center gap-1.5">
                  <Building2 className="w-3.5 h-3.5 text-cyan-400" />
                  <span>Workspaces</span>
                </span>
                {!isGuest && (
                  <button
                    onClick={() => setShowNewWsInput(!showNewWsInput)}
                    className="text-xs font-medium text-cyan-400 hover:text-cyan-300 flex items-center gap-1"
                  >
                    <Plus className="w-3 h-3" />
                    <span>New</span>
                  </button>
                )}
              </div>

              {/* New Workspace Input */}
              {showNewWsInput && (
                <form onSubmit={handleCreateWorkspace} className="mb-3 flex gap-2">
                  <input
                    type="text"
                    required
                    placeholder="Workspace Name..."
                    value={newWsName}
                    onChange={(e) => setNewWsName(e.target.value)}
                    className="flex-1 px-3 py-1.5 bg-slate-800 border border-slate-700 rounded-lg text-xs text-white placeholder-slate-500 focus:outline-none focus:border-cyan-500"
                  />
                  <button
                    type="submit"
                    className="px-3 py-1.5 bg-cyan-600 hover:bg-cyan-500 text-white rounded-lg text-xs font-medium"
                  >
                    Create
                  </button>
                </form>
              )}

              {/* Workspace List */}
              <div className="space-y-1.5">
                {workspaces.map((ws) => {
                  const isSelected = activeWorkspace?.id === ws.id;
                  return (
                    <button
                      key={ws.id}
                      onClick={() => {
                        setActiveWorkspace(ws);
                        onWorkspaceChange(ws);
                      }}
                      className={`w-full flex items-center justify-between p-2.5 rounded-xl border text-left transition-all ${
                        isSelected
                          ? "bg-slate-800/90 border-cyan-500/50 shadow-md shadow-cyan-500/5"
                          : "bg-slate-850/40 border-slate-800 hover:border-slate-700 text-slate-300"
                      }`}
                    >
                      <div className="flex items-center gap-2.5">
                        <div className="w-7 h-7 rounded-lg bg-slate-800 border border-slate-700 flex items-center justify-center text-xs font-bold text-slate-300">
                          {ws.name[0]}
                        </div>
                        <div>
                          <div className="text-xs font-medium text-white">{ws.name}</div>
                          <div className="text-[10px] text-slate-400 capitalize">{ws.role} Role</div>
                        </div>
                      </div>
                      {isSelected && <Check className="w-4 h-4 text-cyan-400" />}
                    </button>
                  );
                })}
              </div>
            </div>

            {/* Team Members Section */}
            <div>
              <div className="flex items-center justify-between mb-3">
                <span className="text-xs font-semibold uppercase tracking-wider text-slate-400 flex items-center gap-1.5">
                  <Users className="w-3.5 h-3.5 text-indigo-400" />
                  <span>Team Members ({members.length})</span>
                </span>
                <span className="text-[10px] px-2 py-0.5 rounded-full bg-slate-800 text-slate-400 border border-slate-700">
                  {userRole.toUpperCase()}
                </span>
              </div>

              {/* Invite Form (Admin/Owner only) */}
              {canManageTeam && !isGuest && (
                <form onSubmit={handleInvite} className="mb-4 p-3 bg-slate-800/40 rounded-xl border border-slate-800 space-y-2">
                  <div className="text-[11px] font-medium text-slate-300 flex items-center gap-1">
                    <UserPlus className="w-3 h-3 text-cyan-400" />
                    <span>Invite Team Member</span>
                  </div>
                  <div className="flex gap-2">
                    <input
                      type="email"
                      required
                      placeholder="teammate@company.com"
                      value={inviteEmail}
                      onChange={(e) => setInviteEmail(e.target.value)}
                      className="flex-1 px-3 py-1.5 bg-slate-800 border border-slate-700 rounded-lg text-xs text-white placeholder-slate-500 focus:outline-none focus:border-cyan-500"
                    />
                    <select
                      value={inviteRole}
                      onChange={(e) => setInviteRole(e.target.value as WorkspaceRole)}
                      className="px-2 py-1.5 bg-slate-800 border border-slate-700 rounded-lg text-xs text-slate-300 focus:outline-none focus:border-cyan-500"
                    >
                      <option value="analyst">Analyst</option>
                      <option value="viewer">Viewer</option>
                      <option value="admin">Admin</option>
                    </select>
                  </div>
                  <button
                    type="submit"
                    className="w-full py-1.5 bg-indigo-600 hover:bg-indigo-500 text-white rounded-lg text-xs font-medium transition-colors"
                  >
                    Send Invitation
                  </button>
                </form>
              )}

              {/* Member List */}
              <div className="space-y-2">
                {loadingMembers ? (
                  <div className="text-center py-6 text-xs text-slate-500">Loading members...</div>
                ) : members.length === 0 ? (
                  <div className="text-center py-6 text-xs text-slate-500">No members found in this workspace.</div>
                ) : (
                  members.map((m) => {
                    const isSelf = m.user_id === currentUser?.id;
                    return (
                      <div
                        key={m.id}
                        className="flex items-center justify-between p-2.5 bg-slate-800/30 rounded-xl border border-slate-800 hover:border-slate-750 transition-all"
                      >
                        <div className="flex items-center gap-2.5 min-w-0">
                          <div className="w-7 h-7 rounded-lg bg-slate-800 flex items-center justify-center text-xs font-medium text-slate-300">
                            {m.full_name ? m.full_name[0].toUpperCase() : m.email[0].toUpperCase()}
                          </div>
                          <div className="min-w-0">
                            <div className="text-xs font-medium text-white truncate flex items-center gap-1.5">
                              <span>{m.full_name || m.email}</span>
                              {isSelf && (
                                <span className="text-[9px] px-1.5 py-0.2 rounded bg-cyan-950 text-cyan-400 border border-cyan-800">
                                  You
                                </span>
                              )}
                            </div>
                            <div className="text-[10px] text-slate-500 truncate">{m.email}</div>
                          </div>
                        </div>

                        <div className="flex items-center gap-2">
                          {canManageTeam && !isSelf && m.role !== "owner" ? (
                            <select
                              value={m.role}
                              onChange={(e) => handleUpdateRole(m.user_id, e.target.value)}
                              className="px-2 py-1 bg-slate-800 border border-slate-700 rounded text-[11px] text-slate-300 focus:outline-none"
                            >
                              <option value="admin">Admin</option>
                              <option value="analyst">Analyst</option>
                              <option value="viewer">Viewer</option>
                            </select>
                          ) : (
                            <span
                              className={`text-[10px] px-2 py-0.5 rounded-full font-medium ${
                                m.role === "owner"
                                  ? "bg-amber-950/80 text-amber-400 border border-amber-800"
                                  : m.role === "admin"
                                  ? "bg-purple-950/80 text-purple-400 border border-purple-800"
                                  : m.role === "analyst"
                                  ? "bg-cyan-950/80 text-cyan-400 border border-cyan-800"
                                  : "bg-slate-800 text-slate-400 border border-slate-700"
                              }`}
                            >
                              {m.role}
                            </span>
                          )}

                          {canManageTeam && !isSelf && m.role !== "owner" && (
                            <button
                              onClick={() => handleRemoveMember(m.user_id)}
                              className="p-1 text-slate-500 hover:text-rose-400 rounded transition-colors"
                              title="Remove member"
                            >
                              <Trash2 className="w-3.5 h-3.5" />
                            </button>
                          )}
                        </div>
                      </div>
                    );
                  })
                )}
              </div>
            </div>
          </div>

          {/* Drawer Footer */}
          <div className="p-4 border-t border-slate-800 bg-slate-900/90">
            {isGuest ? (
              <button
                onClick={() => {
                  onClose();
                  onOpenAuth();
                }}
                className="w-full py-2.5 px-4 bg-gradient-to-r from-cyan-600 to-indigo-600 hover:from-cyan-500 hover:to-indigo-500 text-white font-medium text-xs rounded-xl shadow-lg shadow-indigo-600/20 transition-all flex items-center justify-center gap-2"
              >
                <Shield className="w-4 h-4" />
                <span>Sign In / Create Account</span>
              </button>
            ) : (
              <button
                onClick={handleSignOut}
                className="w-full py-2.5 px-4 bg-slate-800 hover:bg-rose-950/50 border border-slate-700 hover:border-rose-800 text-slate-300 hover:text-rose-300 font-medium text-xs rounded-xl transition-all flex items-center justify-center gap-2"
              >
                <LogOut className="w-4 h-4" />
                <span>Sign Out</span>
              </button>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};
