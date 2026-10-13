# MOI QUEST — Moment of Inertia Learning Game

A dark, neon-accented Streamlit learning game for rotational mechanics by **Aman Edge Physics**.

## Features
- Mission Control dashboard and session XP
- Animated canvas rotor in the Spin Lab
- Interactive 3D geometry lab with play/pause tracer animation, rotation-axis display, and body comparison
- Torque Duel prediction game with side-by-side body comparisons, live inertia/acceleration values, and XP
- Live calculations for common bodies and axes
- Challenge Arena with 12 conceptual questions and explanations
- Formula Vault and field manual
- Global footer credit: Aman Kumar Patel / Aman Edge Physics

## Run locally
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy on Streamlit Community Cloud
1. Open the repository on GitHub.
2. Select **Add file → Create new file** if you need to edit files.
3. Ensure `app.py` and `requirements.txt` are in the repository root.
4. Open Streamlit Community Cloud and sign in with GitHub.
5. Choose **Create app**, select this repository, branch `main`, and main file path `app.py`.
6. Deploy. Your students can then open the generated app URL.

## Physics model
The simulation assumes a rigid body, fixed axis, constant net torque and no speed-dependent drag. The animation is illustrative; numerical outputs use `alpha = net_torque / I` and constant-angular-acceleration kinematics.


### Dynamics Arena
- Select symmetry, transverse, or offset parallel axes.
- Explore torque, opposing friction, angular velocity and rotational kinetic energy plots.
- The 3D animation rotates the complete displayed surface mesh around the selected axis; its play/pause loop is a visual aid and is not yet time-synchronized to the computed angular-velocity curve.
- Optional shared leaderboard uses Supabase when configured; otherwise scores are session-local.
