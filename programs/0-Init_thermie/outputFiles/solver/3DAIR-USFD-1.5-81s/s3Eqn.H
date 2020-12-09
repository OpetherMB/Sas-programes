fvScalarMatrix s3Eqn
(
fvm::ddt(s3)
+ fvm::div(phi, s3)
- fvm::laplacian(Ds+turbulence->nut()/Sct, s3)
==
fvOptions(s3)
);

s3Eqn.relax();
fvOptions.constrain(s3Eqn);
s3Eqn.solve();
fvOptions.correct(s3);
