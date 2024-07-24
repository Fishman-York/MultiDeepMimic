#pragma once

#include "scenes/RLSceneSimChar.h"
#include "anim/KinCharacter.h"
#include "anim/KinCtrlBuilder.h"

class cSceneImitate : virtual public cRLSceneSimChar
{
public:
	EIGEN_MAKE_ALIGNED_OPERATOR_NEW

	cSceneImitate();
	virtual ~cSceneImitate();

	virtual void ParseArgs(const std::shared_ptr<cArgParser>& parser);
	virtual void Init();

	virtual const std::shared_ptr<cKinCharacter>& GetKinChar(int id) const;
	virtual const std::shared_ptr<cKinCharacter>& GetKinChar() const;
	virtual void EnableRandRotReset(bool enable);
	virtual bool EnabledRandRotReset() const;

	virtual double CalcReward(int agent_id) const;
	virtual eTerminate CheckTerminate(int agent_id) const;

	virtual std::string GetName() const;

protected:

	std::vector<cKinCtrlBuilder::tCtrlParams> mKinCtrlParams;
	std::vector<std::shared_ptr<cKinCharacter>> mKinChars;

	Eigen::VectorXd mJointWeights;
	bool mEnableRandRotReset;
	bool mSyncCharRootPos;
	bool mSyncCharRootRot;
	bool mEnableRootRotFail;

	virtual void ParseKinCtrlParams(const std::shared_ptr<cArgParser>& parser, std::vector<cKinCtrlBuilder::tCtrlParams>& out_params) const;
	virtual bool BuildCharacters();

	virtual void CalcJointWeights(const std::shared_ptr<cSimCharacter>& character, Eigen::VectorXd& out_weights) const;
	virtual bool BuildController(int id, const cCtrlBuilder::tCtrlParams& ctrl_params, std::shared_ptr<cCharController>& out_ctrl);
	virtual bool BuildKinCharacters();
	virtual bool BuildKinCharacter(const cKinCharacter::tParams& params, std::shared_ptr<cKinCharacter>& out_char) const;
	virtual bool BuildKinControllers();
	virtual void UpdateCharacters(double timestep);
	virtual void UpdateKinChars(double timestep);
	virtual void UpdateKinChar(int id, double timestep);

	virtual void ResetCharacters();
	virtual void ResetKinChars();
	virtual void ResetKinChar(int id);
	virtual void SyncCharacters();
	virtual void SyncCharacter(int id);
	virtual void EnableSyncChars();
	virtual bool EnableSyncChar(int id) const;
	virtual void InitCharacterPosFixed(const std::shared_ptr<cSimCharacter>& out_char);

	virtual void InitJointWeights();
	virtual void InitJointWeight(int id);
	virtual void ResolveCharGroundIntersect();
	virtual void ResolveCharGroundIntersect(const std::shared_ptr<cSimCharacter>& out_char) const;
	virtual void SyncKinCharRoot(int id);
	virtual void SyncKinCharNewCycle(const cSimCharacter& sim_char, cKinCharacter& out_kin_char) const;

	virtual double GetKinTime(int id) const;
	virtual bool CheckKinNewCycle(int id, double timestep) const;
	virtual bool HasFallen(const cSimCharacter& sim_char) const;
	virtual bool CheckRootRotFail(const cSimCharacter& sim_char) const;
	virtual bool CheckRootRotFail(const cSimCharacter& sim_char, const cKinCharacter& kin_char) const;
	
	virtual double CalcRandKinResetTime(int id);
	virtual double CalcRewardImitate(const cSimCharacter& sim_char, const cKinCharacter& ref_char) const;
};