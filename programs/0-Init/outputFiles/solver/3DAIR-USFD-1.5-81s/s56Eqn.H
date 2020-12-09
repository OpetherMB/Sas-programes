fvScalarMatrix s56Eqn
(
fvm::ddt(s56)
+ fvm::div(phi, s56)
- fvm::laplacian(Ds+turbulence->nut()/Sct, s56)
==
fvOptions(s56)
);

s56Eqn.relax();
fvOptions.constrain(s56Eqn);
s56Eqn.solve();
fvOptions.correct(s56);
